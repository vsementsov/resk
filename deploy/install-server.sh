#!/usr/bin/env bash
# Run as root from a directory containing the deploy files and actions-key.pub.
set -euo pipefail

if ! id resk-deploy >/dev/null 2>&1; then
  useradd --system --create-home --home-dir /var/lib/resk-deploy --shell /bin/sh resk-deploy
fi
install -d -o root -g root -m 755 /usr/local/lib/resk /var/lib/resk-deploy/.ssh
install -m 755 receive_site.py enable_https.py /usr/local/lib/resk/
install -d -o resk-deploy -g resk-deploy -m 755 /var/www/resk /var/www/resk/releases
chown root:root /var/lib/resk-deploy
chmod 755 /var/lib/resk-deploy
python3 - <<'PY'
from pathlib import Path
key = Path('actions-key.pub').read_text().strip()
assert key.startswith('ssh-ed25519 ')
Path('/var/lib/resk-deploy/.ssh/authorized_keys').write_text(
    'restrict,command="/usr/bin/python3 /usr/local/lib/resk/receive_site.py" ' + key + '\n'
)
PY
chown root:root /var/lib/resk-deploy/.ssh/authorized_keys
chmod 644 /var/lib/resk-deploy/.ssh/authorized_keys

install -d -m 755 /etc/caddy/sites-available /etc/caddy/sites-enabled
install -m 644 resk.caddy /etc/caddy/sites-available/resk-https.caddy
install -m 644 resk-http.caddy /etc/caddy/sites-enabled/resk.caddy
if ! test -e /etc/caddy/Caddyfile.before-resk; then
  cp -a /etc/caddy/Caddyfile /etc/caddy/Caddyfile.before-resk
fi
printf 'import /etc/caddy/sites-enabled/*.caddy\n' > /etc/caddy/Caddyfile
caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile
systemctl enable --now caddy
systemctl reload caddy

cat > /etc/systemd/system/resk-dns.service <<'UNIT'
[Unit]
Description=Enable RESK HTTPS after domain DNS points to VDSina
After=network-online.target caddy.service
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /usr/local/lib/resk/enable_https.py
UNIT
cat > /etc/systemd/system/resk-dns.timer <<'UNIT'
[Unit]
Description=Wait for RESK DNS before requesting a TLS certificate

[Timer]
OnBootSec=1min
OnUnitActiveSec=1min
AccuracySec=10s
Unit=resk-dns.service

[Install]
WantedBy=timers.target
UNIT
systemctl daemon-reload
systemctl enable --now resk-dns.timer
systemctl start resk-dns.service
