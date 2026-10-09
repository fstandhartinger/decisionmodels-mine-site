#!/usr/bin/env python3
"""Render doctor samples offline from the checksum-verified, pinned kit archive.
Fixture injection mirrors tests/test_core_doctor.py; the real CLI emits the text.
Run after release-kit.py whenever the pinned kit changes. No kit checkout is edited.
"""
import argparse
import contextlib
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def render(kit, fixture_name):
    sys.path.insert(0, str(kit))
    from reaxlib.cli import main
    fixture = json.loads((kit/'tests/fixtures'/fixture_name).read_text())
    def probe(cmd, timeout=0.4):
        return fixture['commands'].get(' '.join(cmd), {'returncode': 127, 'stdout': '', 'stderr': 'not found'})
    with tempfile.TemporaryDirectory(prefix='dm-doctor-home-') as home:
        output = io.StringIO()
        with patch('reaxlib.sysprobe.run', side_effect=probe), patch('reaxlib.sysprobe.facts', return_value=fixture['host']), patch('urllib.request.urlopen', side_effect=AssertionError('Sample doctor must remain offline')), contextlib.redirect_stdout(output):
            code = main(['doctor', '--home', home])
        if code != 0:
            raise SystemExit('Fixture doctor failed: '+output.getvalue())
        return output.getvalue()


def generate():
    lock = json.loads((ROOT/'kit.lock.json').read_text())
    archive = ROOT/'site/kit'/lock['tarball']
    if hashlib.sha256(archive.read_bytes()).hexdigest() != lock['sha256']:
        raise SystemExit('Pinned kit archive checksum mismatch')
    samples = ROOT/'content/samples'; samples.mkdir(parents=True, exist_ok=True)
    receipts = {}
    with tempfile.TemporaryDirectory(prefix='dm-sample-kit-') as temporary:
        kit = Path(temporary)
        with tarfile.open(archive) as tar:
            tar.extractall(kit, filter='data')
        for ident, fixture in [('4090', 'core_4090.json'), ('no-gpu', 'core_no_gpu.json')]:
            output = subprocess.check_output([sys.executable, str(Path(__file__).resolve()), '--render', str(kit), fixture], text=True)
            (samples/('doctor-'+ident+'.txt')).write_text(output)
            receipts[ident] = {'fixture': 'tests/fixtures/'+fixture, 'fixture_sha256': hashlib.sha256((kit/'tests/fixtures'/fixture).read_bytes()).hexdigest(), 'output_sha256': hashlib.sha256(output.encode()).hexdigest(), 'excerpt': False}
    (samples/'provenance.json').write_text(json.dumps({'kit_commit': lock['commit'], 'kit_version': lock['version'], 'archive_sha256': lock['sha256'], 'path': 'reaxlib.cli.main → cmd_doctor.diagnose → result.emit (fixture sysprobe injection)', 'samples': receipts}, indent=2)+'\n')
    print('Generated 2 offline CLI samples from pinned kit '+lock['commit'])


if __name__ == '__main__':
    if len(sys.argv) == 4 and sys.argv[1] == '--render':
        print(render(Path(sys.argv[2]), sys.argv[3]), end='')
    else:
        generate()
