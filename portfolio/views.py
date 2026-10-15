import json
import logging

from django.contrib import messages
from django.db import DatabaseError, connection
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET

from .forms import ContactForm
from .highlight import highlight_code
from .i18n import DEFAULT_LANGUAGE, LANGUAGES, get_ui, normalize_language
from .icons import LAYER_ICONS, PRINCIPLE_ICONS
from .models import AboutCard, ContactMessage, Metric, Profile, Project, Skill, TimelineItem
from .services import get_client_ip, is_rate_limited, notify_owner

logger = logging.getLogger(__name__)

HOME_URL_NAMES = {"ru": "home", "uz": "home_uz"}


def home_url(lang: str) -> str:
    return reverse(HOME_URL_NAMES[normalize_language(lang)])


def _developer_profile_code(profile: Profile, lang: str, skills: list[Skill]) -> str:
    stack = ", ".join(f'"{s.name.split(" ")[0]}"' for s in skills[:7]) or '"Python"'
    lines = [
        "from dataclasses import dataclass",
        "",
        "",
        "@dataclass(frozen=True, slots=True)",
        "class PythonDeveloper:",
        f'    full_name: str = "{profile.full_name}"',
        f'    role: str = "{profile.role}"',
    ]
    if profile.age:
        lines.append(f"    age: int = {profile.age}")
    lines.append(f'    location: str = "{profile.tr("city", lang)}"')
    lines.append(f"    core_stack: tuple[str, ...] = ({stack})")
    if profile.telegram_handle:
        lines.append(f'    telegram: str = "{profile.telegram_handle}"')
    lines.append(f'    email: str = "{profile.email}"')
    lines.append(f"    open_to_work: bool = {profile.is_available}")
    return "\n".join(lines)


def _json_ld(profile: Profile, lang: str) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": profile.full_name,
        "jobTitle": profile.role,
        "email": f"mailto:{profile.email}",
        "address": {"@type": "PostalAddress", "addressLocality": profile.tr("city", lang)},
        "sameAs": [
            url
            for url in (profile.github_url, profile.linkedin_url, profile.telegram_url, profile.instagram_url)
            if url
        ],
    }
    # Escape "<" so the JSON can never close the surrounding <script> tag.
    return json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")


def _number_sections(keys: list[str]) -> dict[str, str]:
    return {key: f"{index:02d}" for index, key in enumerate(keys, start=1)}


def home(request, lang: str = DEFAULT_LANGUAGE):
    lang = normalize_language(lang)
    t = get_ui(lang)
    profile = Profile.load()

    skills = list(Skill.objects.filter(is_active=True))
    projects = list(Project.objects.filter(is_published=True))
    timeline = list(TimelineItem.objects.all())

    section_keys = ["about", "skills", "projects", "architecture"]
    if timeline:
        section_keys.append("experience")
    section_keys.append("contacts")

    layers = [
        {**layer, "icon": LAYER_ICONS.get(layer["key"], "layers")}
        for layer in t["architecture"]["layers"]
    ]
    principles = [
        {**item, "icon": PRINCIPLE_ICONS[i % len(PRINCIPLE_ICONS)]}
        for i, item in enumerate(t["architecture"]["principles"])
    ]

    name_parts = profile.full_name.rsplit(" ", 1) if profile else ["", ""]
    if len(name_parts) == 1:
        name_parts = ["", name_parts[0]]

    context = {
        "lang": lang,
        "t": t,
        "profile": profile,
        "hero_badges": (
            ["Python"] + [part.strip() for part in profile.specialization.split("/") if part.strip()][:3]
            if profile
            else []
        ),
        "name_head": name_parts[0],
        "name_tail": name_parts[1],
        "metrics": list(Metric.objects.all()),
        "about_cards": list(AboutCard.objects.all()),
        "skills": skills,
        "skill_categories": [c for c, _ in Skill.CATEGORY_CHOICES if any(s.category == c for s in skills)],
        "projects": projects,
        "timeline": timeline,
        "layers": layers,
        "principles": principles,
        "section_numbers": _number_sections(section_keys),
        "developer_code": highlight_code(_developer_profile_code(profile, lang, skills), "python")
        if profile
        else "",
        "json_ld": _json_ld(profile, lang) if profile else "",
        "alternate_urls": {code: home_url(code) for code in LANGUAGES},
        "current_year": timezone.localdate().year,
    }
    return render(request, "portfolio/home.html", context)


def _wants_json(request) -> bool:
    accept = request.headers.get("Accept", "")
    return (
        request.headers.get("X-Requested-With") == "XMLHttpRequest"
        or "application/json" in accept
    )


def contact_submit(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    lang = normalize_language(request.POST.get("lang"))
    t = get_ui(lang)["contacts"]["form"]
    wants_json = _wants_json(request)
    back_url = home_url(lang) + "#contacts"

    def respond(ok: bool, message: str, status: int = 200, errors: dict | None = None):
        if wants_json:
            payload = {"ok": ok, "message": message}
            if errors:
                payload["errors"] = errors
            return JsonResponse(payload, status=status)
        (messages.success if ok else messages.error)(request, message)
        return redirect(back_url)

    form = ContactForm(request.POST, lang=lang)

    # Bots that fill the honeypot get a fake success and nothing is stored.
    if form.is_spam:
        return respond(True, t["success"])

    ip = get_client_ip(request)
    if is_rate_limited(ip):
        return respond(False, t["rate_limited"], status=429)

    if not form.is_valid():
        errors = {field: [str(e) for e in errs] for field, errs in form.errors.items()}
        if not wants_json:
            first = next(iter(errors.values()))[0]
            return respond(False, first)
        return respond(False, t["invalid"], status=400, errors=errors)

    try:
        msg = ContactMessage.objects.create(
            name=form.cleaned_data["name"],
            contact=form.cleaned_data["contact"],
            message=form.cleaned_data["message"],
            language=lang,
            ip_address=ip,
            user_agent=request.headers.get("User-Agent", "")[:300],
        )
    except DatabaseError:
        logger.exception("Could not store contact message")
        return respond(False, t["error"], status=500)

    notify_owner(msg)
    return respond(True, t["success"])


def _absolute(request, url: str) -> str:
    return request.build_absolute_uri(url) if url else ""


@require_GET
@cache_control(public=True, max_age=60)
def api_portfolio(request):
    """Read-only JSON with the whole portfolio, e.g. for a Telegram bot or mobile app."""
    lang = normalize_language(request.GET.get("lang"))
    profile = Profile.load()
    if profile is None:
        return JsonResponse({"detail": "Portfolio is not configured yet."}, status=404)

    data = {
        "language": lang,
        "profile": {
            "full_name": profile.full_name,
            "role": profile.role,
            "specialization": profile.specialization,
            "age": profile.age,
            "city": profile.tr("city", lang),
            "description": profile.tr("hero_description", lang),
            "is_available": profile.is_available,
            "availability": profile.tr("availability", lang),
            "contacts": {
                "email": profile.email,
                "phone": profile.phone_raw,
                "telegram": profile.telegram_handle,
                "telegram_url": profile.telegram_url,
                "github": profile.github_url,
                "linkedin": profile.linkedin_url,
                "instagram": profile.instagram_url,
            },
            "cv_url": _absolute(request, profile.cv_file.url) if profile.cv_file else "",
        },
        "metrics": [
            {"value": m.value, "unit": m.tr("unit", lang), "label": m.tr("label", lang)}
            for m in Metric.objects.all()
        ],
        "about": [
            {
                "title": c.tr("title", lang),
                "lead": c.tr("lead", lang),
                "body": c.tr("body", lang),
                "meta": c.tr("meta", lang),
            }
            for c in AboutCard.objects.all()
        ],
        "skills": [
            {
                "slug": s.slug,
                "name": s.name,
                "category": s.category,
                "level": s.level,
                "experience": s.tr("experience", lang),
            }
            for s in Skill.objects.filter(is_active=True)
        ],
        "projects": [
            {
                "slug": p.slug,
                "title": p.title,
                "subtitle": p.tr("subtitle", lang),
                "description": p.tr("description", lang),
                "architecture": p.tr("architecture", lang),
                "metrics": p.metrics,
                "year": p.year,
                "tags": p.tag_list,
                "image": _absolute(request, p.image.url) if p.image else "",
                "github_url": p.github_url,
                "demo_url": p.demo_url,
            }
            for p in Project.objects.filter(is_published=True)
        ],
        "experience": [
            {
                "kind": item.kind,
                "title": item.tr("title", lang),
                "organization": item.organization,
                "period": item.period,
                "description": item.tr("description", lang),
            }
            for item in TimelineItem.objects.all()
        ],
    }
    return JsonResponse(data, json_dumps_params={"ensure_ascii": False})


@require_GET
def healthz(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except DatabaseError:
        return JsonResponse({"status": "error", "database": "unavailable"}, status=503)
    return JsonResponse({"status": "ok"})


@require_GET
def robots_txt(request):
    from django.conf import settings

    lines = [
        "User-agent: *",
        f"Disallow: /{settings.ADMIN_URL}",
        "Disallow: /api/",
        "Allow: /",
        f"Sitemap: {request.build_absolute_uri(reverse('sitemap'))}",
    ]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain")


def _error_context(request) -> dict:
    lang = "uz" if request.path.startswith("/uz/") else DEFAULT_LANGUAGE
    return {"lang": lang, "t": get_ui(lang), "home": home_url(lang)}


def page_not_found(request, exception=None):
    return render(request, "404.html", _error_context(request), status=404)


def server_error(request):
    return render(request, "500.html", _error_context(request), status=500)
