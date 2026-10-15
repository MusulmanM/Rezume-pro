# Rezume-pro — My Rezume

Musulmankulov Musulmanning shaxsiy portfolio / rezyume sayti (Python Developer).
Django monolit: sahifa server tomonda render qilinadi, barcha kontent admin paneldan boshqariladi.

## Imkoniyatlar

- **Ikki til** — `/` (ruscha) va `/uz/` (o‘zbekcha), `hreflang`, sitemap.
- **Bo‘limlar** — Hero (video showreel), ko‘rsatkichlar, Men haqimda, Ko‘nikmalar (kod namunalari bilan),
  Loyihalar (modal oynada arxitektura va kod), Arxitektura (so‘rov yo‘li), Tajriba (ixtiyoriy), Aloqa.
- **Kontakt forma** — xabar bazaga yoziladi va darhol **Telegram** (va ixtiyoriy Email) ga yuboriladi.
  Himoya: CSRF, honeypot, IP bo‘yicha rate-limit (+ nginx `limit_req`), validatsiya.
- **Admin panel** — profil, video, rezyume PDF, ko‘rsatkichlar, ko‘nikmalar, loyihalar, tajriba, kelgan xabarlar.
- **JSON API** — `GET /api/portfolio/?lang=uz` (bot yoki mobil ilova uchun).
- `GET /healthz/`, `robots.txt`, `sitemap.xml`, 404/500 sahifalari.
- Kod bloklari serverda Pygments bilan rang beriladi; rasmlar seed paytida WebP ga o‘tkaziladi.

## Lokal ishga tushirish

```bash
python -m venv venv
venv\Scripts\activate            # Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
echo DEBUG=true > .env
python manage.py migrate
python manage.py seed_portfolio  # boshlang‘ich kontent (rasm va video bilan)
python manage.py createsuperuser
python manage.py runserver
```

Sayt: http://127.0.0.1:8000/ · Admin: http://127.0.0.1:8000/admin/

Testlar: `python manage.py test portfolio`

## Serverga joylash (Ubuntu / Debian)

Loyihani serverga `/srv/rezume-pro` ga joylang (git clone yoki yuklash), keyin:

```bash
cd /srv/rezume-pro
sudo bash deploy/setup.sh example.uz www.example.uz   # yoki faqat IP: sudo bash deploy/setup.sh 203.0.113.10
```

Skript: paketlar, `rezume` foydalanuvchisi, venv, `.env` (SECRET_KEY va admin yo‘li avtomatik yaratiladi),
migratsiya, static, seed, systemd (`rezume.service`, gunicorn) va nginx ni sozlaydi, oxirida health-check qiladi.

Keyingi yangilanishlar: `sudo bash deploy/update.sh`

### Telegram xabarnomalar

1. @BotFather orqali bot yarating va tokenni oling.
2. Botga istalgan xabar yozing, so‘ng `https://api.telegram.org/bot<TOKEN>/getUpdates` dan `chat.id` ni oling.
3. `.env` ga `TELEGRAM_BOT_TOKEN` va `TELEGRAM_CHAT_ID` ni yozing → `sudo systemctl restart rezume`.

### HTTPS

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d example.uz -d www.example.uz
```

So‘ng `.env` da `USE_HTTPS=true`, `SECURE_SSL_REDIRECT=true` qilib, `sudo systemctl restart rezume`.

## Tuzilma

```
config/                 Django sozlamalari (barchasi .env orqali)
portfolio/
  models.py             Profile, Metric, AboutCard, Skill, Project, TimelineItem, ContactMessage
  views.py              sahifa, kontakt forma, API, healthz, robots
  services.py           rate-limit, Telegram / Email xabarnoma
  i18n.py               interfeys matnlari (RU / UZ)
  seed_data.py          boshlang‘ich kontent; seed_media/ — rasm va video
templates/              shablonlar (portfolio/partials/*)
static/                 css/main.css, js/main.js, img/favicon.svg
deploy/                 setup.sh, update.sh, nginx.conf, rezume.service, gunicorn.conf.py
```
