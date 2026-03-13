from django.contrib import admin
from django.urls import include, path
from django.views.static import serve

from mmmoney import views


HTDOCS = "htdocs"

urlpatterns = [
    path("accounts/oauth/", views.oauth),
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("favicon.ico", serve, {"document_root": HTDOCS, "path": "favicon.ico"}),
    path("favicon.png", serve, {"document_root": HTDOCS, "path": "favicon.png"}),
    path("icon.svg", serve, {"document_root": HTDOCS, "path": "icon.svg"}),
    path(
        "apple-touch-icon.png",
        serve,
        {"document_root": HTDOCS, "path": "apple-touch-icon.png"},
    ),
    path("icon-192.png", serve, {"document_root": HTDOCS, "path": "icon-192.png"}),
    path("icon-512.png", serve, {"document_root": HTDOCS, "path": "icon-512.png"}),
    path("manifest.json", serve, {"document_root": HTDOCS, "path": "manifest.json"}),
    path("", include("mmmoney.resources")),
]
