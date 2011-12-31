from django.conf.urls import patterns, include, url
from django.contrib import admin

from mmmoney.views import entry_views


admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include(entry_views.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
