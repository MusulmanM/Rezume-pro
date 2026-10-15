from django.contrib import admin
from django.utils.html import format_html
from django.utils.text import Truncator

from .models import AboutCard, ContactMessage, Metric, Profile, Project, Skill, TimelineItem

admin.site.site_header = "My Rezume — boshqaruv paneli"
admin.site.site_title = "My Rezume admin"
admin.site.index_title = "Sayt kontentini boshqarish"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Asosiy", {"fields": ("full_name", "role", "specialization", "age", "city_ru", "city_uz")}),
        ("Brend", {"fields": ("site_name", "logo_short")}),
        (
            "Hero bo'limi",
            {
                "fields": (
                    "hero_description_ru",
                    "hero_description_uz",
                    "is_available",
                    "availability_ru",
                    "availability_uz",
                    "hero_video",
                    "hero_poster",
                    "cv_file",
                )
            },
        ),
        (
            "Aloqa",
            {
                "fields": (
                    "email",
                    "phone_display",
                    "phone_raw",
                    "telegram_handle",
                    "telegram_url",
                    "telegram_channel_url",
                )
            },
        ),
        ("Ijtimoiy tarmoqlar", {"fields": ("github_url", "linkedin_url", "instagram_url")}),
        ("SEO", {"fields": ("meta_description_ru", "meta_description_uz")}),
    )

    def has_add_permission(self, request):
        return not Profile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ("value", "unit_uz", "label_uz", "order")
    list_editable = ("order",)


@admin.register(AboutCard)
class AboutCardAdmin(admin.ModelAdmin):
    list_display = ("title_uz", "title_ru", "icon", "order")
    list_editable = ("order",)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "level", "is_active", "order")
    list_editable = ("is_active", "order")
    list_filter = ("category", "is_active")
    search_fields = ("name", "experience_ru", "experience_uz")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("thumbnail", "title", "year", "is_published", "order")
    list_display_links = ("thumbnail", "title")
    list_editable = ("is_published", "order")
    list_filter = ("is_published", "year")
    search_fields = ("title", "tags", "description_ru", "description_uz")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (None, {"fields": ("title", "slug", "year", "is_published", "order")}),
        ("Tavsif", {"fields": ("subtitle_ru", "subtitle_uz", "description_ru", "description_uz")}),
        ("Arxitektura", {"fields": ("architecture_ru", "architecture_uz", "metrics")}),
        ("Vizual", {"fields": ("image", "accent")}),
        ("Havolalar va teglar", {"fields": ("tags", "github_url", "demo_url")}),
        ("Kod", {"fields": ("code_filename", "code_language", "code_preview")}),
    )

    @admin.display(description="Rasm")
    def thumbnail(self, obj):
        if not obj.image:
            return "—"
        return format_html(
            '<img src="{}" alt="" style="width:72px;height:45px;object-fit:cover;border-radius:6px">',
            obj.image.url,
        )


@admin.register(TimelineItem)
class TimelineItemAdmin(admin.ModelAdmin):
    list_display = ("organization", "title_uz", "kind", "period", "order")
    list_editable = ("order",)
    list_filter = ("kind",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "contact_link",
        "short_message",
        "status",
        "language",
        "telegram_delivered",
        "created_at",
    )
    list_filter = ("status", "language", "telegram_delivered", "created_at")
    search_fields = ("name", "contact", "message")
    date_hierarchy = "created_at"
    readonly_fields = (
        "name",
        "contact",
        "message",
        "language",
        "ip_address",
        "user_agent",
        "telegram_delivered",
        "email_delivered",
        "created_at",
    )
    fields = readonly_fields[:3] + ("status",) + readonly_fields[3:]
    actions = ("mark_read", "mark_replied", "mark_spam")

    def has_add_permission(self, request):
        return False

    @admin.display(description="Aloqa")
    def contact_link(self, obj):
        value = obj.contact
        if value.startswith("@"):
            return format_html('<a href="https://t.me/{}" target="_blank" rel="noopener">{}</a>', value[1:], value)
        if "@" in value:
            return format_html('<a href="mailto:{}">{}</a>', value, value)
        return format_html('<a href="tel:{}">{}</a>', value.replace(" ", ""), value)

    @admin.display(description="Xabar")
    def short_message(self, obj):
        return Truncator(obj.message).chars(70)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        if str(object_id).isdigit():
            ContactMessage.objects.filter(pk=object_id, status=ContactMessage.STATUS_NEW).update(
                status=ContactMessage.STATUS_READ
            )
        return super().change_view(request, object_id, form_url, extra_context)

    @admin.action(description="O'qilgan deb belgilash")
    def mark_read(self, request, queryset):
        queryset.update(status=ContactMessage.STATUS_READ)

    @admin.action(description="Javob berilgan deb belgilash")
    def mark_replied(self, request, queryset):
        queryset.update(status=ContactMessage.STATUS_REPLIED)

    @admin.action(description="Spam deb belgilash")
    def mark_spam(self, request, queryset):
        queryset.update(status=ContactMessage.STATUS_SPAM)
