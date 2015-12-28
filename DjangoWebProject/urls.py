"""
Definition of urls for DjangoWebProject.
"""

from datetime import datetime
from django.conf.urls import patterns, url
from django.conf.urls import include
from django.contrib import admin
from . import settings

# Устанавливает заголовок (из settins.py) в админке
admin.site.site_header = settings.ADMIN_SITE_HEADER

admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'app.views.home', name='home'),

    # Jet
    url(r'^jet/', include('jet.urls', 'jet')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Admin
    url(r'^admin/', include(admin.site.urls)),
)
