#!/usr/bin/env python3
"""Bounded local HTTP checks of our own generated nginx config; no deployment."""
from pathlib import Path
import shutil
import socket
import subprocess
import tempfile
import time
import urllib.error
import urllib.request

ROOT=Path(__file__).resolve().parents[1]

def main():
    nginx=shutil.which('nginx')
    if not nginx: print('SKIP: nginx unavailable'); return
    with tempfile.TemporaryDirectory(prefix='decisionmodels-site-check-') as scratch:
        directory=Path(scratch)
        with socket.socket() as sock: sock.bind(('127.0.0.1',0)); port=sock.getsockname()[1]
        config=(ROOT/'dist/nginx.conf').read_text().replace('listen 8080;',f'listen 127.0.0.1:{port};').replace('/usr/share/nginx/html',str(ROOT/'dist')).replace('/tmp/nginx.pid',str(directory/'nginx.pid'))
        # Testing as a non-root user needs job-local temp/cache paths.
        config=config.replace('http {','http {\n    client_body_temp_path '+str(directory/'body')+';\n    proxy_temp_path '+str(directory/'proxy')+';\n    fastcgi_temp_path '+str(directory/'fastcgi')+';\n    uwsgi_temp_path '+str(directory/'uwsgi')+';\n    scgi_temp_path '+str(directory/'scgi')+';')
        path=directory/'nginx.conf';path.write_text(config)
        subprocess.run([nginx,'-t','-c',str(path),'-p',str(directory)],check=True)
        proc=subprocess.Popen([nginx,'-c',str(path),'-p',str(directory),'-g','daemon off;'],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
        base=f'http://127.0.0.1:{port}'
        def get(path,accept=None):
            request=urllib.request.Request(base+path,headers={'Accept':accept} if accept else {})
            try: return urllib.request.urlopen(request,timeout=3)
            except urllib.error.HTTPError as error: return error
        try:
            for _ in range(40):
                try:
                    with get('/healthz') as response: assert response.read()==b'ok\n';break
                except OSError: time.sleep(.1)
            else: raise RuntimeError('nginx did not start')
            for route in ['/','/agent','/os/linux','/os/windows','/os/macos','/wallets','/rewards-and-risks','/troubleshooting']:
                with get(route) as response:
                    assert response.status==200 and response.headers.get_content_type()=='text/html',route
                    assert response.headers['X-Robots-Tag']=='noindex, nofollow'
                    assert 'unsafe-inline' not in response.headers['Content-Security-Policy']
                with get(route,'text/markdown') as response:
                    twin='index.md' if route=='/' else route.lstrip('/')+'.md'
                    assert response.status==200,route
                    assert response.read()==(ROOT/'dist'/twin).read_bytes(),route
                    assert response.headers.get_content_type()=='text/markdown',dict(response.headers)
                    assert response.headers['Vary']=='Accept'
            for route in ['/not-a-guide', '/404', '/404.html']:
                with get(route) as response:
                    assert response.status==404, route
                    body=response.read().decode()
                    assert 'ON THIS PAGE' not in body and 'Read as Markdown' not in body
            with get('/agent.md') as response: assert response.headers.get_content_type()=='text/markdown'
            with get('/mine.json') as response: assert response.headers.get_content_type()=='application/json'
            print('PASS: nginx syntax, healthz, 8 HTML/Markdown negotiations, MIME, Vary, CSP, launch hold and 404')
            # Reuse the same local nginx instance for browser tests if requested.
            import sys
            if '--screenshots' in sys.argv:
                target=Path(sys.argv[sys.argv.index('--screenshots')+1])
                subprocess.run(['python3',str(ROOT/'scripts/screenshot.py'),'--url',base,'--output',str(target)]+(['--isolated'] if '--isolated' in sys.argv else []),check=True,timeout=150)
        finally:
            proc.terminate()
            try: proc.communicate(timeout=5)
            except subprocess.TimeoutExpired: proc.kill();proc.communicate()

if __name__=='__main__': main()
