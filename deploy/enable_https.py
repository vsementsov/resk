#!/usr/bin/python3
"""Enable the prepared HTTPS site only after DNS points solely to this VPS."""
from pathlib import Path
import shutil
import socket
import subprocess

DOMAIN = 'xn--e1akqf.xn--p1ai'
IP = '212.193.14.81'
READY = Path('/etc/caddy/sites-available/resk-https.caddy')
ACTIVE = Path('/etc/caddy/sites-enabled/resk.caddy')

def main():
    try:
        addresses = {item[4][0] for item in socket.getaddrinfo(DOMAIN, 443, type=socket.SOCK_STREAM)}
    except socket.gaierror:
        print('Waiting for domain DNS')
        return
    if addresses != {IP}:
        print('Waiting for A to point to VDSina and stale AAAA to be removed')
        return
    if ACTIVE.read_bytes() != READY.read_bytes():
        subprocess.run(['caddy', 'validate', '--config', str(READY), '--adapter', 'caddyfile'], check=True)
        previous = ACTIVE.read_bytes()
        shutil.copyfile(READY, ACTIVE)
        result = subprocess.run(['systemctl', 'reload', 'caddy'])
        if result.returncode:
            ACTIVE.write_bytes(previous)
            raise RuntimeError('Caddy reload failed; HTTP configuration restored')
        print('DNS is ready: automatic HTTPS enabled')
    subprocess.run(['systemctl', 'disable', '--now', 'resk-dns.timer'], check=True)

if __name__ == '__main__':
    main()
