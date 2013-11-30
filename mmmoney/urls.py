from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from mmmoney.views import entry_views


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'', include(entry_views.urls)),
    url(r'^admin/', include(admin.site.urls)),
) + staticfiles_urlpatterns()
