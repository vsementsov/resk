#!/usr/bin/python3
"""Restricted SSH receiver: deploy <40-character commit>, tar.gz on stdin."""
import fcntl
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sys
import tarfile
import tempfile
import time

BASE = Path('/var/www/resk')
LIMIT = 32 * 1024 * 1024

def deploy():
    match = re.fullmatch(r'deploy ([a-f0-9]{40})', os.environ.get('SSH_ORIGINAL_COMMAND', ''))
    if not match:
        raise ValueError('Only deploy <commit> is allowed')
    commit = match.group(1)
    with (BASE / '.deploy.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        stage = Path(tempfile.mkdtemp(prefix='.incoming-', dir=BASE))
        try:
            with tempfile.TemporaryFile() as stream:
                size = 0
                while chunk := sys.stdin.buffer.read(65536):
                    size += len(chunk)
                    if size > LIMIT:
                        raise ValueError('Archive exceeds size limit')
                    stream.write(chunk)
                stream.seek(0)
                with tarfile.open(fileobj=stream, mode='r|gz') as archive:
                    unpacked = 0
                    seen = set()
                    for count, member in enumerate(archive, 1):
                        unpacked += member.size
                        if count > 2000 or unpacked > LIMIT:
                            raise ValueError('Unpacked site exceeds size limit')
                        path = PurePosixPath(member.name)
                        if path.is_absolute() or '..' in path.parts or not (member.isfile() or member.isdir()):
                            raise ValueError('Unsafe archive member')
                        if path in seen:
                            raise ValueError('Duplicate archive member')
                        seen.add(path)
                        target = stage.joinpath(*path.parts)
                        if member.isdir():
                            target.mkdir(parents=True, exist_ok=True)
                        else:
                            target.parent.mkdir(parents=True, exist_ok=True)
                            with archive.extractfile(member) as source, target.open('wb') as output:
                                shutil.copyfileobj(source, output)
                            target.chmod(0o644)
            for required in ['index.html', 'architecture.css', 'style.css', 'script.js', 'assets/logo.svg']:
                if not (stage / required).is_file():
                    raise ValueError(f'Missing required file: {required}')
            (stage / 'deploy-version.json').write_text(json.dumps({'commit': commit}) + '\n')
            for directory, _, _ in os.walk(stage):
                Path(directory).chmod(0o755)
            releases = BASE / 'releases'
            releases.mkdir(exist_ok=True)
            release = releases / f'{commit}-{time.time_ns()}'
            stage.rename(release)
            link = BASE / '.current-next'
            link.unlink(missing_ok=True)
            link.symlink_to(release)
            link.replace(BASE / 'current')
            # Keep five complete releases for administrator rollback.
            for old in sorted(releases.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)[5:]:
                if old.is_dir() and old != release:
                    shutil.rmtree(old)
            print(f'Deployed {commit}', flush=True)
        finally:
            if stage.exists():
                shutil.rmtree(stage)

if __name__ == '__main__':
    try:
        deploy()
    except Exception as error:
        print(f'Deploy failed: {error}', file=sys.stderr)
        sys.exit(1)
