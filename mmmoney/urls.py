from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path

from mmmoney import views


urlpatterns = [
    re_path(r"^accounts/oauth/", views.oauth),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("mmmoney.resources")),
    re_path(r"^admin/", admin.site.urls),
] + staticfiles_urlpatterns()
