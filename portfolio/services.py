"""Side effects of the contact form: throttling and owner notifications."""

import json
import logging
import urllib.error
import urllib.request

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.utils.html import escape

from .models import ContactMessage

logger = logging.getLogger(__name__)

TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"
TELEGRAM_LIMIT = 4000  # Telegram hard limit is 4096 characters per message


def get_client_ip(request) -> str | None:
    """Client IP. Behind nginx the real address is the last X-Forwarded-For hop."""
    if getattr(settings, "TRUST_X_FORWARDED_FOR", False):
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if forwarded:
            return forwarded.split(",")[-1].strip() or None
        real_ip = request.META.get("HTTP_X_REAL_IP", "").strip()
        if real_ip:
            return real_ip
    return request.META.get("REMOTE_ADDR") or None


def is_rate_limited(ip: str | None) -> bool:
    """Fixed-window limiter: CONTACT_RATE_LIMIT messages per CONTACT_RATE_WINDOW seconds per IP."""
    limit = settings.CONTACT_RATE_LIMIT
    if limit <= 0:
        return False
    key = f"contact-rate:{ip or 'unknown'}"
    window = settings.CONTACT_RATE_WINDOW
    if cache.add(key, 1, timeout=window):
        return False
    try:
        count = cache.incr(key)
    except ValueError:  # key expired between add() and incr()
        cache.set(key, 1, timeout=window)
        return False
    return count > limit


def _telegram_text(msg: ContactMessage) -> str:
    text = (
        "📩 <b>Yangi xabar — My Rezume</b>\n\n"
        f"👤 <b>{escape(msg.name)}</b>\n"
        f"📞 {escape(msg.contact)}\n"
        f"🌐 Til: {escape(msg.language.upper())}\n\n"
        f"{escape(msg.message)}"
    )
    if len(text) > TELEGRAM_LIMIT:
        text = text[: TELEGRAM_LIMIT - 1] + "…"
    return text


def send_telegram(msg: ContactMessage) -> bool:
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    if not token or not chat_id:
        return False
    payload = json.dumps(
        {
            "chat_id": chat_id,
            "text": _telegram_text(msg),
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        TELEGRAM_API.format(token=token),
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=6) as response:
            body = json.loads(response.read().decode("utf-8"))
            if not body.get("ok"):
                logger.warning("Telegram rejected contact message %s: %s", msg.pk, body)
                return False
            return True
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
        logger.warning("Telegram notification failed for message %s: %s", msg.pk, exc)
        return False


def send_email_notification(msg: ContactMessage) -> bool:
    recipient = settings.CONTACT_NOTIFY_EMAIL
    if not recipient:
        return False
    try:
        send_mail(
            subject=f"My Rezume — yangi xabar: {msg.name}",
            message=(
                f"Ism: {msg.name}\n"
                f"Aloqa: {msg.contact}\n"
                f"Til: {msg.language}\n"
                f"IP: {msg.ip_address or '-'}\n\n"
                f"{msg.message}\n"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
        return True
    except Exception as exc:  # SMTP errors come in many flavours; never break the request
        logger.warning("Email notification failed for message %s: %s", msg.pk, exc)
        return False


def notify_owner(msg: ContactMessage) -> None:
    telegram_ok = send_telegram(msg)
    email_ok = send_email_notification(msg)
    if telegram_ok or email_ok:
        ContactMessage.objects.filter(pk=msg.pk).update(
            telegram_delivered=telegram_ok, email_delivered=email_ok
        )
        msg.telegram_delivered = telegram_ok
        msg.email_delivered = email_ok
