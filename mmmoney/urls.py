from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'', include('mmmoney.resources')),
    url(r'^admin/', include(admin.site.urls)),
) + staticfiles_urlpatterns()
