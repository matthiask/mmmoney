from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'', include('mmmoney.resources')),
    url(r'^admin/', include(admin.site.urls)),
] + staticfiles_urlpatterns()
