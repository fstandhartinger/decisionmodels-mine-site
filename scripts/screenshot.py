#!/usr/bin/env python3
"""Review our unpublished site in the shared Sandy browser; closes only its own tab.
Use --url for an nginx instance, or a temporary loopback static server is started.
--isolated is opt-in only for briefs that explicitly permit headless Chrome.
"""
import argparse
import contextlib
import fcntl
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import threading
import time
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]

class StaticHandler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs): super().__init__(*args,directory=str(ROOT/'dist'),**kwargs)
    def do_GET(self):
        path=urlsplit(self.path).path
        candidate=ROOT/'dist'/path.lstrip('/')
        if not candidate.exists() and candidate.with_suffix('.html').is_file(): self.path=path+'.html'
        super().do_GET()
    def log_message(self,*args): pass

@contextlib.contextmanager
def static_server():
    server=ThreadingHTTPServer(('127.0.0.1',0),StaticHandler)
    thread=threading.Thread(target=server.serve_forever,daemon=True); thread.start()
    try: yield 'http://127.0.0.1:'+str(server.server_port)
    finally: server.shutdown(); server.server_close(); thread.join()

def capture(url,output,cdp,isolated=False):
    output.mkdir(parents=True,exist_ok=True)
    checks=[]
    with open(Path.home()/'.locks/chrome-9333.lock','r') as lock:
        deadline=time.monotonic()+90
        while not isolated:
            try:
                fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB); break
            except BlockingIOError:
                if time.monotonic()>deadline: raise SystemExit('Shared Chrome lock unavailable after 90 seconds; no extra browser started.')
                time.sleep(1)
        with sync_playwright() as pw:
            browser = pw.chromium.launch(executable_path='/usr/bin/google-chrome', headless=True, args=['--no-sandbox']) if isolated else pw.chromium.connect_over_cdp(cdp)
            context = browser.new_context() if isolated else browser.contexts[0]
            page=context.new_page()
            errors=[]; page.on('pageerror',lambda error: errors.append(str(error)))
            page.on('console', lambda message: errors.append(message.text) if message.type == 'error' else None)
            try:
                for width,label in [(1440,'desk'),(390,'mob')]:
                    page.set_viewport_size({'width':width,'height':1000 if width==1440 else 844})
                    for theme in ['light','dark']:
                        page.emulate_media(color_scheme=theme,reduced_motion='reduce')
                        page.goto(url+'/',wait_until='networkidle')
                        page.evaluate("localStorage.removeItem('dm-theme')")
                        page.reload(wait_until='networkidle')
                        page.evaluate('document.fonts.ready')
                        assert page.locator('h1').count()==1
                        assert not page.evaluate('document.documentElement.scrollWidth > innerWidth'),f'Overflow {label} {theme}'
                        page.screenshot(path=str(output/f'{label}-{theme}.png'),full_page=True)
                        if width == 1440: page.screenshot(path=str(output/f'{label}-{theme}-top.png'))
                        for sample in ['4090', 'no-gpu']:
                            page.locator('[data-sample="'+sample+'"]').click()
                            assert page.locator('#doctor-'+sample).is_visible()
                            other = 'no-gpu' if sample == '4090' else '4090'
                            assert not page.locator('#doctor-'+other).is_visible()
                            page.locator('.doctor-samples').screenshot(path=str(output/f'{label}-{theme}-doctor-{sample}.png'))
                        page.locator('[data-sample="4090"]').click()
                        checks.append(f'{label} {theme}: no horizontal overflow; screenshot captured')
                page.locator('[data-sample="4090"]').focus()
                page.keyboard.press('ArrowRight')
                assert page.locator('#doctor-no-gpu').is_visible()
                page.keyboard.press('Home')
                assert page.locator('#doctor-4090').is_visible()
                checks.append('Doctor tabs support keyboard navigation')
                page.get_by_role('button',name='Safe by default',exact=True).click()
                assert 'reference material' in page.locator('#agent-prompt').inner_text()
                page.get_by_role('button',name='Short',exact=True).click()
                assert page.locator('#agent-prompt').inner_text()=='Set up this machine for mining at Decision Models by REAX: https://mine.decisionmodels.io'
                # Clipboard access is not granted automatically; the UI has a selectable-text fallback.
                page.get_by_role('button',name='Copy prompt',exact=True).click()
                assert page.locator('.copy-status').inner_text()
                checks.append('Prompt variants and copy/fallback passed')
                for os in ['linux','windows','macos']:
                    page.select_option('#os',os); page.select_option('#gpu','24')
                    assert page.locator('#os-guide').get_attribute('href')=='/os/'+os
                    assert page.locator('.checker').get_attribute('action')=='/os/'+os
                    verdict=page.locator('#verdict').inner_text()
                    assert 'not live' in verdict
                    if os=='windows': assert 'not yet tested by us' in verdict
                    if os=='macos': assert 'cannot mine' in verdict
                page.select_option('#os','linux');page.select_option('#gpu','amd')
                assert 'another host' in page.locator('#verdict').inner_text()
                checks.append('OS/GPU matrix and launch hold passed')
                for mode in ['Light','Dark','Auto']:
                    page.locator('.theme-toggle').click()
                    assert page.locator('.theme-toggle').inner_text() == mode
                    page.reload(wait_until='networkidle')
                    assert page.locator('.theme-toggle').inner_text() == mode
                    assert page.evaluate('localStorage.getItem("dm-theme")') == mode.lower()
                checks.append('Light / Dark / Auto cycle and persistence passed; both doctor tabs captured at each viewport/theme')
                page.goto(url+'/agent',wait_until='networkidle')
                assert page.locator('pre button').count()>0
                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth')
                page.screenshot(path=str(output/'mobile-agent.png'),full_page=True)
                checks.append('Agent docs code-copy controls and mobile layout passed')
                # Disable scripts on our own tab, rather than creating another browser profile/context.
                session=page.context.new_cdp_session(page)
                session.send('Emulation.setScriptExecutionDisabled',{'value':True})
                page.goto(url+'/',wait_until='networkidle')
                assert page.locator('#agent-prompt').is_visible()
                assert page.get_by_role('button',name='Windows guide',exact=True).is_visible()
                page.get_by_role('button',name='Windows guide',exact=True).click()
                page.wait_for_url('**/os/windows?*')
                assert page.locator('h1').inner_text().startswith('Windows')
                checks.append('No-JS selectable prompt and OS guide navigation passed')
                session.send('Emulation.setScriptExecutionDisabled',{'value':False})
                if errors: raise AssertionError(errors)
                checks.append('No browser JavaScript or console errors')
            finally:
                page.close()
                if isolated: browser.close()
                # The shared browser belongs to other jobs and is never closed.
        fcntl.flock(lock,fcntl.LOCK_UN)
    (output/'browser-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    print('\n'.join(checks))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--url');parser.add_argument('--isolated',action='store_true',help='Explicit opt-in: temporary headless Chrome for screenshot jobs that authorize it');parser.add_argument('--output',type=Path,default=ROOT/'shots');parser.add_argument('--cdp',default='http://127.0.0.1:9333');args=parser.parse_args()
    if args.url: capture(args.url,args.output,args.cdp,args.isolated)
    else:
        with static_server() as url: capture(url,args.output,args.cdp,args.isolated)
