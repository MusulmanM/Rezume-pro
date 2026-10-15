from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Profile


class HomeSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    i18n = False

    def items(self):
        return ["home", "home_uz"]

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        profile = Profile.load()
        return profile.updated_at if profile else None
