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

handler400 = 'app.views.error400'
handler403 = 'app.views.error403'
#handler404 = 'app.views.error404'
#handler500 = 'app.views.error500'

urlpatterns = patterns('',

    #url(r'^$', 'app.views.index', name='index'),
    #url(r'^manage/$', 'app.views.manage', name='manage'),
    #url(r'^steward/$', 'app.views.steward', name='steward'),

    # AJAX
    url(r'^ajax/create_weeks/$', 'attendance.views.createWeeks'),

    # Аутентификация
    url(r'^login/$', 'accounts.views.login', name='login'),
    url(r'^logout/$', 'accounts.views.logout', name='logout'),

    # Jet
    url(r'^jet/', include('jet.urls', 'jet')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Admin
    url(r'^admin/', include(admin.site.urls)),
)
