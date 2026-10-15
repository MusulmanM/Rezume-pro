import io
import json
import shutil
import tempfile
from unittest import mock

from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from .forms import ContactForm
from .models import ContactMessage, Profile, Project, Skill

TEMP_MEDIA = tempfile.mkdtemp(prefix="rezume-test-media-")


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class SeededTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_portfolio", verbosity=0, stdout=io.StringIO())

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA, ignore_errors=True)

    def setUp(self):
        cache.clear()


class SeedCommandTests(SeededTestCase):
    def test_seed_creates_content_and_media(self):
        profile = Profile.load()
        self.assertIsNotNone(profile)
        self.assertEqual(profile.full_name, "Musulmankulov Musulman")
        self.assertTrue(profile.hero_video.name.endswith(".mp4"))
        self.assertTrue(profile.hero_poster.name.endswith(".webp"))
        self.assertEqual(Skill.objects.count(), 12)
        self.assertEqual(Project.objects.count(), 4)
        self.assertTrue(all(p.image for p in Project.objects.all()))

    def test_seed_is_idempotent_without_force(self):
        call_command("seed_portfolio", verbosity=0, stdout=io.StringIO())
        self.assertEqual(Project.objects.count(), 4)
        self.assertEqual(Profile.objects.count(), 1)

    def test_profile_is_singleton(self):
        Profile(full_name="Other", city_ru="x", city_uz="x", hero_description_ru="x",
                hero_description_uz="x", email="a@b.cd").save()
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.load().full_name, "Other")


class PageTests(SeededTestCase):
    def test_home_ru(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<html lang="ru"')
        self.assertContains(response, "Технологический арсенал")
        self.assertContains(response, "Nexus Commerce Microservices API")
        self.assertContains(response, 'hreflang="uz"')
        self.assertContains(response, 'class="ln"')  # highlighted code

    def test_home_uz(self):
        response = self.client.get(reverse("home_uz"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<html lang="uz"')
        self.assertContains(response, "Texnologik stek")
        self.assertContains(response, "Toshkent, O‘zbekiston")

    def test_unpublished_project_hidden(self):
        Project.objects.filter(slug="nexus-commerce-api").update(is_published=False)
        response = self.client.get(reverse("home"))
        self.assertNotContains(response, "Nexus Commerce Microservices API")

    def test_home_without_profile_shows_setup_notice(self):
        Profile.objects.all().delete()  # queryset delete bypasses the model guard
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "seed_portfolio")

    def test_404_page(self):
        response = self.client.get("/does-not-exist/")
        self.assertEqual(response.status_code, 404)

    def test_service_endpoints(self):
        self.assertEqual(self.client.get(reverse("healthz")).json(), {"status": "ok"})
        robots = self.client.get(reverse("robots_txt"))
        self.assertContains(robots, "Sitemap:")
        sitemap = self.client.get(reverse("sitemap"))
        self.assertContains(sitemap, "/uz/")

    def test_json_ld_is_valid_json(self):
        response = self.client.get(reverse("home"))
        data = json.loads(response.context["json_ld"])
        self.assertEqual(data["@type"], "Person")


class ApiTests(SeededTestCase):
    def test_portfolio_api(self):
        response = self.client.get(reverse("api_portfolio"), {"lang": "uz"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["language"], "uz")
        self.assertEqual(data["profile"]["city"], "Toshkent, O‘zbekiston")
        self.assertEqual(len(data["projects"]), 4)
        self.assertTrue(data["projects"][0]["image"].startswith("http://testserver/media/"))

    def test_unknown_language_falls_back_to_ru(self):
        data = self.client.get(reverse("api_portfolio"), {"lang": "xx"}).json()
        self.assertEqual(data["language"], "ru")

    def test_api_is_read_only(self):
        self.assertEqual(self.client.post(reverse("api_portfolio")).status_code, 405)


@override_settings(TELEGRAM_BOT_TOKEN="", TELEGRAM_CHAT_ID="", CONTACT_NOTIFY_EMAIL="")
class ContactTests(SeededTestCase):
    url = "/contact/"
    ajax = {"HTTP_X_REQUESTED_WITH": "XMLHttpRequest", "HTTP_ACCEPT": "application/json"}
    valid = {"name": "Ali", "contact": "@ali_dev", "message": "Assalomu alaykum, loyiha bor.", "lang": "uz"}

    def test_valid_message_is_stored(self):
        response = self.client.post(self.url, self.valid, **self.ajax)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["ok"])
        msg = ContactMessage.objects.get()
        self.assertEqual(msg.contact, "@ali_dev")
        self.assertEqual(msg.language, "uz")
        self.assertEqual(msg.ip_address, "127.0.0.1")

    def test_telegram_username_without_at_is_normalized(self):
        self.client.post(self.url, {**self.valid, "contact": "ali_dev"}, **self.ajax)
        self.assertEqual(ContactMessage.objects.get().contact, "@ali_dev")

    def test_email_and_phone_contacts_accepted(self):
        for contact in ("ali@example.com", "+998 90 123 45 67"):
            response = self.client.post(self.url, {**self.valid, "contact": contact}, **self.ajax)
            self.assertEqual(response.status_code, 200, contact)
        self.assertEqual(ContactMessage.objects.count(), 2)

    def test_invalid_message_returns_localized_errors(self):
        response = self.client.post(
            self.url, {"name": "", "contact": "nope!", "message": "hi", "lang": "ru"}, **self.ajax
        )
        self.assertEqual(response.status_code, 400)
        errors = response.json()["errors"]
        self.assertEqual(set(errors), {"name", "contact", "message"})
        self.assertIn("Укажите имя", errors["name"][0])
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_message_too_long(self):
        response = self.client.post(self.url, {**self.valid, "message": "x" * 3001}, **self.ajax)
        self.assertEqual(response.status_code, 400)
        self.assertIn("message", response.json()["errors"])

    def test_honeypot_pretends_success_but_stores_nothing(self):
        response = self.client.post(self.url, {**self.valid, "website": "http://spam"}, **self.ajax)
        self.assertTrue(response.json()["ok"])
        self.assertEqual(ContactMessage.objects.count(), 0)

    @override_settings(CONTACT_RATE_LIMIT=2)
    def test_rate_limit(self):
        for _ in range(2):
            self.assertEqual(self.client.post(self.url, self.valid, **self.ajax).status_code, 200)
        response = self.client.post(self.url, self.valid, **self.ajax)
        self.assertEqual(response.status_code, 429)
        self.assertEqual(ContactMessage.objects.count(), 2)

    def test_get_not_allowed(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_csrf_is_enforced(self):
        client = self.client_class(enforce_csrf_checks=True)
        self.assertEqual(client.post(self.url, self.valid, **self.ajax).status_code, 403)

    def test_non_js_fallback_redirects_with_message(self):
        response = self.client.post(self.url, self.valid, follow=True)
        self.assertRedirects(response, reverse("home_uz") + "#contacts")
        self.assertContains(response, "Rahmat!")

    @override_settings(TELEGRAM_BOT_TOKEN="123:abc", TELEGRAM_CHAT_ID="42")
    def test_telegram_notification_success(self):
        fake = mock.MagicMock()
        fake.__enter__.return_value.read.return_value = b'{"ok": true}'
        with mock.patch("portfolio.services.urllib.request.urlopen", return_value=fake) as urlopen:
            self.client.post(self.url, {**self.valid, "message": "<b>salom</b> test xabar"}, **self.ajax)
        request = urlopen.call_args[0][0]
        payload = json.loads(request.data)
        self.assertEqual(payload["chat_id"], "42")
        self.assertIn("&lt;b&gt;salom&lt;/b&gt;", payload["text"])  # user input is escaped
        self.assertTrue(ContactMessage.objects.get().telegram_delivered)

    @override_settings(TELEGRAM_BOT_TOKEN="123:abc", TELEGRAM_CHAT_ID="42")
    def test_telegram_failure_does_not_break_request(self):
        import urllib.error

        with mock.patch(
            "portfolio.services.urllib.request.urlopen", side_effect=urllib.error.URLError("down")
        ):
            response = self.client.post(self.url, self.valid, **self.ajax)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ContactMessage.objects.get().telegram_delivered)

    @override_settings(TRUST_X_FORWARDED_FOR=True)
    def test_client_ip_from_proxy(self):
        self.client.post(self.url, self.valid, HTTP_X_FORWARDED_FOR="1.1.1.1, 203.0.113.7", **self.ajax)
        self.assertEqual(ContactMessage.objects.get().ip_address, "203.0.113.7")


class ContactFormUnitTests(TestCase):
    def test_contact_formats(self):
        def valid(contact):
            form = ContactForm({"name": "A", "contact": contact, "message": "0123456789"}, lang="ru")
            return form.is_valid()

        self.assertTrue(valid("@user_name"))
        self.assertTrue(valid("name@mail.uz"))
        self.assertTrue(valid("+998958011060"))
        self.assertFalse(valid("@ab"))
        self.assertFalse(valid("not an email@"))
        self.assertFalse(valid("hello world"))


class AdminTests(SeededTestCase):
    def setUp(self):
        super().setUp()
        from django.contrib.auth.models import User

        self.admin = User.objects.create_superuser("admin", "admin@example.com", "pass12345")
        self.client.force_login(self.admin)

    def test_admin_pages_render(self):
        ContactMessage.objects.create(name="A", contact="@abcde", message="hello there")
        for model in ("profile", "metric", "aboutcard", "skill", "project", "timelineitem", "contactmessage"):
            url = reverse(f"admin:portfolio_{model}_changelist")
            self.assertEqual(self.client.get(url).status_code, 200, model)

    def test_opening_message_marks_it_read(self):
        msg = ContactMessage.objects.create(name="A", contact="@abcde", message="hello there")
        url = reverse("admin:portfolio_contactmessage_change", args=[msg.pk])
        self.assertEqual(self.client.get(url).status_code, 200)
        msg.refresh_from_db()
        self.assertEqual(msg.status, ContactMessage.STATUS_READ)

    def test_profile_cannot_be_added_twice(self):
        self.assertEqual(self.client.get(reverse("admin:portfolio_profile_add")).status_code, 403)
