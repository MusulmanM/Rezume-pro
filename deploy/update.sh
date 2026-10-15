#!/usr/bin/env bash
# Deploy a new version after the code on the server was updated (git pull / upload).
#   sudo bash deploy/update.sh
set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_USER="rezume"

chown -R "$APP_USER:$APP_USER" "$APP_DIR"
run() { sudo -H -u "$APP_USER" bash -c "cd '$APP_DIR' && $*"; }

run "venv/bin/pip install --no-cache-dir -r requirements.txt -q"
run "venv/bin/python manage.py migrate --noinput"
run "venv/bin/python manage.py collectstatic --noinput -v 0"
chmod -R o+rX "$APP_DIR/staticfiles" "$APP_DIR/media"

systemctl restart rezume
sleep 2
systemctl is-active --quiet rezume && echo "rezume: running" || { journalctl -u rezume -n 50 --no-pager; exit 1; }
