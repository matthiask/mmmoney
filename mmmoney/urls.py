from django.contrib import admin
from django.urls import include, path

from mmmoney import views


urlpatterns = [
    path("accounts/oauth/", views.oauth),
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("", include("mmmoney.resources")),
]
