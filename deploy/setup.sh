#!/usr/bin/env bash
# First-time server setup for My Rezume (Ubuntu / Debian).
#
# Usage (as root, from the project directory on the server):
#   sudo bash deploy/setup.sh example.uz www.example.uz
#   sudo bash deploy/setup.sh 203.0.113.10          # IP only, no domain yet
#
# Safe to re-run: it updates code dependencies, migrations, static files and configs.
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
  echo "Run as root: sudo bash deploy/setup.sh <domain-or-ip> [more names...]" >&2
  exit 1
fi
if [[ $# -lt 1 ]]; then
  echo "Usage: sudo bash deploy/setup.sh <domain-or-ip> [more names...]" >&2
  exit 1
fi

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_USER="rezume"
SERVER_NAMES="$*"
FIRST_NAME="$1"

echo "==> App dir: $APP_DIR  |  server_name: $SERVER_NAMES"

echo "==> System packages"
apt-get update -y
apt-get install -y python3 python3-venv python3-pip nginx

PY_OK=$(python3 -c 'import sys; print(int(sys.version_info >= (3, 10)))')
if [[ "$PY_OK" != "1" ]]; then
  echo "Python 3.10+ is required (found $(python3 --version))." >&2
  exit 1
fi

echo "==> App user"
id -u "$APP_USER" >/dev/null 2>&1 || useradd --system --home-dir "$APP_DIR" --shell /usr/sbin/nologin "$APP_USER"

echo "==> Virtualenv & dependencies"
[[ -d "$APP_DIR/venv" ]] || python3 -m venv "$APP_DIR/venv"
"$APP_DIR/venv/bin/pip" install --upgrade pip -q
"$APP_DIR/venv/bin/pip" install -r "$APP_DIR/requirements.txt" -q

echo "==> .env"
if [[ ! -f "$APP_DIR/.env" ]]; then
  cp "$APP_DIR/.env.example" "$APP_DIR/.env"
  SECRET=$("$APP_DIR/venv/bin/python" -c 'import secrets; print(secrets.token_urlsafe(50))')
  HOSTS="$(echo "$SERVER_NAMES" | tr ' ' ','),127.0.0.1,localhost"
  ORIGINS=""
  for name in $SERVER_NAMES; do ORIGINS="${ORIGINS:+$ORIGINS,}http://$name,https://$name"; done
  ADMIN_PATH="admin-$("$APP_DIR/venv/bin/python" -c 'import secrets; print(secrets.token_hex(4))')/"
  sed -i \
    -e "s|^SECRET_KEY=.*|SECRET_KEY=$SECRET|" \
    -e "s|^ALLOWED_HOSTS=.*|ALLOWED_HOSTS=$HOSTS|" \
    -e "s|^CSRF_TRUSTED_ORIGINS=.*|CSRF_TRUSTED_ORIGINS=$ORIGINS|" \
    -e "s|^ADMIN_URL=.*|ADMIN_URL=$ADMIN_PATH|" \
    "$APP_DIR/.env"
  echo "    created .env (admin panel: /$ADMIN_PATH) — add TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID later"
else
  echo "    .env exists, left untouched"
fi
chmod 600 "$APP_DIR/.env"

mkdir -p "$APP_DIR/media" "$APP_DIR/var/cache" "$APP_DIR/staticfiles"
chown -R "$APP_USER:$APP_USER" "$APP_DIR"

run() { sudo -H -u "$APP_USER" bash -c "cd '$APP_DIR' && venv/bin/python manage.py $*"; }

echo "==> Django: check, migrate, static, seed"
run check --deploy --fail-level ERROR
run migrate --noinput
run collectstatic --noinput -v 0
run seed_portfolio

echo "==> systemd"
sed -e "s|__APP_DIR__|$APP_DIR|g" -e "s|__APP_USER__|$APP_USER|g" \
  "$APP_DIR/deploy/rezume.service" > /etc/systemd/system/rezume.service
systemctl daemon-reload
systemctl enable rezume >/dev/null
systemctl restart rezume

echo "==> nginx"
sed -e "s|__APP_DIR__|$APP_DIR|g" -e "s|__SERVER_NAME__|$SERVER_NAMES|g" \
  "$APP_DIR/deploy/nginx.conf" > /etc/nginx/sites-available/rezume
ln -sf /etc/nginx/sites-available/rezume /etc/nginx/sites-enabled/rezume
# nginx (www-data) must be able to read static and media files
chmod o+x "$APP_DIR"
chmod -R o+rX "$APP_DIR/staticfiles" "$APP_DIR/media"
nginx -t
systemctl reload nginx

echo "==> Health check"
sleep 2
if curl -fsS -H "Host: $FIRST_NAME" http://127.0.0.1/healthz/ >/dev/null; then
  echo "    OK — site is up at http://$FIRST_NAME/"
else
  echo "    Health check failed. Logs: journalctl -u rezume -n 50 --no-pager" >&2
  exit 1
fi

cat <<EOF

Next steps:
  1. Create the admin user:
       sudo -u $APP_USER bash -c "cd $APP_DIR && venv/bin/python manage.py createsuperuser"
  2. Telegram notifications: set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in $APP_DIR/.env, then: systemctl restart rezume
  3. HTTPS (domain only): apt install -y certbot python3-certbot-nginx && certbot --nginx -d $FIRST_NAME
     then in .env set USE_HTTPS=true and SECURE_SSL_REDIRECT=true, and restart.
EOF
