from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from mmmoney import views


urlpatterns = [
    url(r"^accounts/oauth/", views.oauth),
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r"", include("mmmoney.resources")),
    url(r"^admin/", admin.site.urls),
] + staticfiles_urlpatterns()
