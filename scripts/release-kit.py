#!/usr/bin/env python3
"""Package a clean, committed kit snapshot. Never executes or modifies the kit."""
import ast
import re
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def main():
    repo = Path(sys.argv[1]).resolve()
    def git(*args):
        return subprocess.check_output(['git', '-C', str(repo), *args])
    if git('status', '--porcelain').strip():
        raise SystemExit('Refusing a dirty kit repository; commit the release first.')
    commit = git('rev-parse', 'HEAD').decode().strip()
    descriptor = git('show', commit + ':releases/current.json')
    release = json.loads(descriptor)
    # Read the literal from the committed source without importing the kit.
    try:
        tree = ast.parse(git('show', commit + ':reaxlib/__init__.py').decode())
        version = next(ast.literal_eval(node.value) for node in tree.body
                       if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == '__version__' for t in node.targets))
    except (StopIteration, ValueError, SyntaxError, subprocess.CalledProcessError):
        raise SystemExit('Kit must define a literal reaxlib.__version__ before packaging.')
    if not isinstance(version, str) or not re.fullmatch(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?', version):
        raise SystemExit('Kit reaxlib.__version__ must be a semantic version (for example 0.1.0).')
    if not version or any(c not in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-+' for c in version):
        raise SystemExit('Unsafe release version')
    name = 'reax-miner-kit-' + version + '.tar.gz'
    # Validate everything above before writing any release artifacts.
    target = ROOT / 'site/kit' / name
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['git', '-C', str(repo), 'archive', '--format=tar.gz', '-o', str(target), commit], check=True)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    (ROOT / 'site/releases').mkdir(parents=True, exist_ok=True)
    (ROOT / 'site/releases/current.json').write_bytes(descriptor)
    lock = dict(version=version, release_id=release['release_id'], commit=commit, sha256=digest, tarball=name, updated=release['updated'])
    (ROOT / 'kit.lock.json').write_text(json.dumps(lock, indent=2) + '\n')
    print(json.dumps(lock, indent=2))

if __name__ == '__main__':
    main()
