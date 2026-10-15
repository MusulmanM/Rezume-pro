from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("", include("portfolio.urls")),
]

if settings.SERVE_MEDIA:
    # In production nginx serves /media/ directly; this is for development or simple setups.
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    ]

handler404 = "portfolio.views.page_not_found"
handler500 = "portfolio.views.server_error"
