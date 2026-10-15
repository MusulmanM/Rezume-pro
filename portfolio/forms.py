import re

from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .i18n import get_ui

TELEGRAM_RE = re.compile(r"^@?[A-Za-z][A-Za-z0-9_]{4,31}$")
PHONE_RE = re.compile(r"^\+?[0-9][0-9 ()\-]{6,18}[0-9]$")

MESSAGE_MIN = 10
MESSAGE_MAX = 3000


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120)
    contact = forms.CharField(max_length=150)
    message = forms.CharField(strip=False)  # length is checked in clean_message
    # Honeypot: real visitors never see or fill this field.
    website = forms.CharField(required=False)

    def __init__(self, *args, lang: str = "ru", **kwargs):
        super().__init__(*args, **kwargs)
        self.lang = lang
        msgs = get_ui(lang)["validation"]
        self.fields["name"].error_messages["required"] = msgs["name_required"]
        self.fields["contact"].error_messages["required"] = msgs["contact_required"]
        self.fields["message"].error_messages["required"] = msgs["message_short"]
        self._msgs = msgs

    @property
    def is_spam(self) -> bool:
        return bool(self.data.get("website", "").strip())

    def clean_name(self) -> str:
        name = " ".join(self.cleaned_data["name"].split())
        if not name:
            raise ValidationError(self._msgs["name_required"])
        return name

    def clean_contact(self) -> str:
        contact = self.cleaned_data["contact"].strip()
        if "@" in contact and not contact.startswith("@"):
            try:
                validate_email(contact)
            except ValidationError:
                raise ValidationError(self._msgs["contact_invalid"])
            return contact
        if TELEGRAM_RE.match(contact):
            return contact if contact.startswith("@") else f"@{contact}"
        if PHONE_RE.match(contact):
            return contact
        raise ValidationError(self._msgs["contact_invalid"])

    def clean_message(self) -> str:
        message = self.cleaned_data["message"].strip()
        if len(message) < MESSAGE_MIN:
            raise ValidationError(self._msgs["message_short"])
        if len(message) > MESSAGE_MAX:
            raise ValidationError(self._msgs["message_long"])
        return message
