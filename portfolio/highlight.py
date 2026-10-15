"""Server-side syntax highlighting for code snippets shown on the site."""

from functools import lru_cache

from django.utils.safestring import SafeString, mark_safe
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

_FORMATTER = HtmlFormatter(nowrap=True)


@lru_cache(maxsize=512)
def _highlight(code: str, language: str) -> str:
    try:
        lexer = get_lexer_by_name(language or "text", stripnl=False)
    except ClassNotFound:
        lexer = get_lexer_by_name("text", stripnl=False)
    # Pygments escapes HTML itself, so the output is safe to embed. Each output line
    # has its token spans closed, so splitting on newlines keeps the markup balanced.
    html = highlight(code, lexer, _FORMATTER).rstrip("\n")
    return "\n".join(f'<span class="ln">{line}</span>' for line in html.split("\n"))


def highlight_code(code: str, language: str = "python") -> SafeString:
    return mark_safe(_highlight(code or "", language))
