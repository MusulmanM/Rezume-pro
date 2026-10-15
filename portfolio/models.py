from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from .i18n import DEFAULT_LANGUAGE, LANGUAGES


class TranslatableMixin:
    """Access `<field>_ru` / `<field>_uz` pairs with a fallback to the default language."""

    def tr(self, field: str, lang: str) -> str:
        if lang not in LANGUAGES:
            lang = DEFAULT_LANGUAGE
        value = getattr(self, f"{field}_{lang}", "")
        if not value and lang != DEFAULT_LANGUAGE:
            value = getattr(self, f"{field}_{DEFAULT_LANGUAGE}", "")
        return value or ""


class OrderedModel(models.Model):
    order = models.PositiveSmallIntegerField("Tartib", default=0, db_index=True)

    class Meta:
        abstract = True
        ordering = ["order", "id"]


class Profile(TranslatableMixin, models.Model):
    """Single-row table holding the site owner's profile and contacts."""

    site_name = models.CharField("Sayt nomi", max_length=60, default="My Rezume")
    logo_short = models.CharField("Logo (qisqa)", max_length=4, default="MR")
    full_name = models.CharField("To'liq ism", max_length=120)
    role = models.CharField("Lavozim", max_length=80, default="Python Developer")
    specialization = models.CharField(
        "Asosiy stek (hero)", max_length=120, default="FastAPI / Django / PostgreSQL"
    )
    age = models.PositiveSmallIntegerField("Yosh", null=True, blank=True)
    city_ru = models.CharField("Shahar (RU)", max_length=80)
    city_uz = models.CharField("Shahar (UZ)", max_length=80)

    hero_description_ru = models.TextField("Hero matni (RU)")
    hero_description_uz = models.TextField("Hero matni (UZ)")
    is_available = models.BooleanField("Ishga ochiq", default=True)
    availability_ru = models.CharField(
        "Holat matni (RU)", max_length=120, default="Открыт для новых предложений"
    )
    availability_uz = models.CharField(
        "Holat matni (UZ)", max_length=120, default="Yangi takliflarga ochiqman"
    )

    email = models.EmailField("Email")
    phone_display = models.CharField("Telefon (ko'rinish)", max_length=40, blank=True)
    phone_raw = models.CharField("Telefon (raqam)", max_length=20, blank=True)
    telegram_handle = models.CharField("Telegram username", max_length=64, blank=True)
    telegram_url = models.URLField("Telegram havola", blank=True)
    telegram_channel_url = models.URLField("Telegram kanal", blank=True)
    github_url = models.URLField("GitHub", blank=True)
    linkedin_url = models.URLField("LinkedIn", blank=True)
    instagram_url = models.URLField("Instagram", blank=True)

    hero_video = models.FileField(
        "Hero video (mp4/webm)",
        upload_to="hero/",
        blank=True,
        validators=[FileExtensionValidator(["mp4", "webm"])],
    )
    hero_poster = models.ImageField("Hero rasm (poster)", upload_to="hero/", blank=True)
    cv_file = models.FileField(
        "Rezyume fayli (PDF)",
        upload_to="cv/",
        blank=True,
        validators=[FileExtensionValidator(["pdf"])],
    )

    meta_description_ru = models.CharField("SEO tavsif (RU)", max_length=300, blank=True)
    meta_description_uz = models.CharField("SEO tavsif (UZ)", max_length=300, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profil"

    def __str__(self) -> str:
        return self.full_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Profilni o'chirib bo'lmaydi.")

    @classmethod
    def load(cls) -> "Profile | None":
        return cls.objects.filter(pk=1).first()

    @property
    def first_name(self) -> str:
        parts = self.full_name.split()
        return parts[-1] if parts else ""


class Metric(TranslatableMixin, OrderedModel):
    value = models.CharField("Qiymat", max_length=16, help_text="Masalan: 15+, 99.9%, < 35")
    unit_ru = models.CharField("Birlik (RU)", max_length=24, blank=True)
    unit_uz = models.CharField("Birlik (UZ)", max_length=24, blank=True)
    label_ru = models.CharField("Izoh (RU)", max_length=80)
    label_uz = models.CharField("Izoh (UZ)", max_length=80)

    class Meta(OrderedModel.Meta):
        verbose_name = "Ko'rsatkich"
        verbose_name_plural = "Ko'rsatkichlar"

    def __str__(self) -> str:
        return f"{self.value} {self.unit_uz}".strip()


class AboutCard(TranslatableMixin, OrderedModel):
    ICON_CHOICES = [
        ("user", "Foydalanuvchi"),
        ("layers", "Qatlamlar"),
        ("globe", "Globus"),
        ("code", "Kod"),
        ("rocket", "Raketa"),
    ]

    icon = models.CharField("Ikonka", max_length=16, choices=ICON_CHOICES, default="user")
    title_ru = models.CharField("Sarlavha (RU)", max_length=60)
    title_uz = models.CharField("Sarlavha (UZ)", max_length=60)
    lead_ru = models.CharField("Asosiy fikr (RU)", max_length=200)
    lead_uz = models.CharField("Asosiy fikr (UZ)", max_length=200)
    body_ru = models.TextField("Matn (RU)")
    body_uz = models.TextField("Matn (UZ)")
    meta_ru = models.CharField("Pastki satr (RU)", max_length=120, blank=True)
    meta_uz = models.CharField("Pastki satr (UZ)", max_length=120, blank=True)

    class Meta(OrderedModel.Meta):
        verbose_name = "Men haqimda kartasi"
        verbose_name_plural = "Men haqimda kartalari"

    def __str__(self) -> str:
        return self.title_uz


CODE_LANGUAGE_CHOICES = [
    ("python", "Python"),
    ("postgresql", "SQL (PostgreSQL)"),
    ("yaml", "YAML"),
    ("nginx", "Nginx"),
    ("docker", "Dockerfile"),
    ("bash", "Bash"),
    ("json", "JSON"),
    ("text", "Oddiy matn"),
]


class Skill(TranslatableMixin, OrderedModel):
    CATEGORY_CHOICES = [
        ("backend", "Backend & Frameworks"),
        ("database", "Databases & Queues"),
        ("devops", "DevOps & Tools"),
    ]

    name = models.CharField("Nomi", max_length=60)
    slug = models.SlugField("Slug", max_length=60, unique=True)
    category = models.CharField("Kategoriya", max_length=16, choices=CATEGORY_CHOICES)
    level = models.CharField("Daraja", max_length=40, blank=True)
    experience_ru = models.TextField("Tajriba (RU)")
    experience_uz = models.TextField("Tajriba (UZ)")
    snippet = models.TextField("Kod namunasi", blank=True)
    snippet_language = models.CharField(
        "Kod tili", max_length=16, choices=CODE_LANGUAGE_CHOICES, default="python"
    )
    is_active = models.BooleanField("Ko'rsatish", default=True)

    class Meta(OrderedModel.Meta):
        verbose_name = "Ko'nikma"
        verbose_name_plural = "Ko'nikmalar"

    def __str__(self) -> str:
        return self.name


class Project(TranslatableMixin, OrderedModel):
    ACCENT_CHOICES = [
        ("cyan", "Cyan → Purple"),
        ("purple", "Purple → Cyan"),
        ("blue", "Cyan → Blue"),
        ("violet", "Violet → Cyan"),
    ]

    slug = models.SlugField("Slug", max_length=80, unique=True)
    title = models.CharField("Nomi", max_length=120)
    subtitle_ru = models.CharField("Qisqa tavsif (RU)", max_length=200)
    subtitle_uz = models.CharField("Qisqa tavsif (UZ)", max_length=200)
    description_ru = models.TextField("Tavsif (RU)")
    description_uz = models.TextField("Tavsif (UZ)")
    architecture_ru = models.TextField("Arxitektura yechimi (RU)", blank=True)
    architecture_uz = models.TextField("Arxitektura yechimi (UZ)", blank=True)
    metrics = models.CharField("Metrikalar", max_length=120, blank=True)
    year = models.CharField("Yil", max_length=9, blank=True)
    image = models.ImageField("Rasm", upload_to="projects/", blank=True)
    accent = models.CharField("Rang aksenti", max_length=10, choices=ACCENT_CHOICES, default="cyan")
    tags = models.CharField("Teglar", max_length=300, blank=True, help_text="Vergul bilan ajrating")
    github_url = models.URLField("GitHub havola", blank=True)
    demo_url = models.URLField("Demo havola", blank=True)
    code_preview = models.TextField("Kod namunasi", blank=True)
    code_language = models.CharField(
        "Kod tili", max_length=16, choices=CODE_LANGUAGE_CHOICES, default="python"
    )
    code_filename = models.CharField("Kod fayli nomi", max_length=80, default="service_handler.py")
    is_published = models.BooleanField("E'lon qilingan", default=True)

    class Meta(OrderedModel.Meta):
        verbose_name = "Loyiha"
        verbose_name_plural = "Loyihalar"

    def __str__(self) -> str:
        return self.title

    @property
    def tag_list(self) -> list[str]:
        return [tag.strip() for tag in self.tags.split(",") if tag.strip()]


class TimelineItem(TranslatableMixin, OrderedModel):
    KIND_CHOICES = [("work", "Ish tajribasi"), ("education", "Ta'lim")]

    kind = models.CharField("Turi", max_length=12, choices=KIND_CHOICES, default="work")
    title_ru = models.CharField("Lavozim / yo'nalish (RU)", max_length=120)
    title_uz = models.CharField("Lavozim / yo'nalish (UZ)", max_length=120)
    organization = models.CharField("Tashkilot", max_length=120)
    period = models.CharField("Davr", max_length=40, help_text="Masalan: 2024 — hozir")
    description_ru = models.TextField("Tavsif (RU)", blank=True)
    description_uz = models.TextField("Tavsif (UZ)", blank=True)

    class Meta(OrderedModel.Meta):
        verbose_name = "Tajriba / ta'lim"
        verbose_name_plural = "Tajriba va ta'lim"

    def __str__(self) -> str:
        return f"{self.organization} — {self.title_uz}"


class ContactMessage(models.Model):
    STATUS_NEW = "new"
    STATUS_READ = "read"
    STATUS_REPLIED = "replied"
    STATUS_SPAM = "spam"
    STATUS_CHOICES = [
        (STATUS_NEW, "Yangi"),
        (STATUS_READ, "O'qilgan"),
        (STATUS_REPLIED, "Javob berilgan"),
        (STATUS_SPAM, "Spam"),
    ]

    name = models.CharField("Ism", max_length=120)
    contact = models.CharField("Aloqa (Telegram / Email)", max_length=150)
    message = models.TextField("Xabar", max_length=3000)
    language = models.CharField("Til", max_length=2, default=DEFAULT_LANGUAGE)
    status = models.CharField(
        "Holat", max_length=10, choices=STATUS_CHOICES, default=STATUS_NEW, db_index=True
    )
    ip_address = models.GenericIPAddressField("IP", null=True, blank=True)
    user_agent = models.CharField("Brauzer", max_length=300, blank=True)
    telegram_delivered = models.BooleanField("Telegramga yuborildi", default=False)
    email_delivered = models.BooleanField("Emailga yuborildi", default=False)
    created_at = models.DateTimeField("Yuborilgan vaqt", auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Xabar"
        verbose_name_plural = "Xabarlar"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} ({self.contact})"
