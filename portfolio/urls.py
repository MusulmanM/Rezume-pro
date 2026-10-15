from django.contrib.sitemaps.views import sitemap
from django.urls import path

from . import views
from .sitemaps import HomeSitemap

urlpatterns = [
    path("", views.home, {"lang": "ru"}, name="home"),
    path("uz/", views.home, {"lang": "uz"}, name="home_uz"),
    path("contact/", views.contact_submit, name="contact"),
    path("api/portfolio/", views.api_portfolio, name="api_portfolio"),
    path("healthz/", views.healthz, name="healthz"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {"home": HomeSitemap}},
        name="sitemap",
    ),
]
