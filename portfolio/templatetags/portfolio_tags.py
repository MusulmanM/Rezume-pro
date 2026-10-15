from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

from ..highlight import highlight_code
from ..icons import ICONS

register = template.Library()


@register.simple_tag
def icon(name: str, size: int = 18, css_class: str = ""):
    """Render an inline Lucide SVG icon: {% icon "github" 16 "extra-class" %}."""
    body = ICONS.get(name)
    if body is None:
        return ""
    classes = f"icon {css_class}".strip()
    return mark_safe(
        f'<svg class="{escape(classes)}" width="{int(size)}" height="{int(size)}" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true" focusable="false">{body}</svg>'
    )


@register.simple_tag(takes_context=True)
def tr(context, obj, field: str):
    """Translated model field for the current page language: {% tr project "title" %}."""
    if obj is None:
        return ""
    return obj.tr(field, context.get("lang", ""))


@register.filter
def highlighted(code: str, language: str = "python"):
    return highlight_code(code, language)
