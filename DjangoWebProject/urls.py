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
handler404 = 'app.views.error404'
handler500 = 'app.views.error500'

urlpatterns = patterns('',

    # Index urls
    # Обратный порядок относительно частоты, зато тег url возвращет красивый url,
    # т.к. берёт последний
    url(r'^default/$', 'app.views.index', name='index'),
    url(r'^main/$', 'app.views.index', name='index'),
    url(r'^index/$', 'app.views.index', name='index'),
    url(r'^$', 'app.views.index', name='index'),

    url(r'^steward/$', 'app.views.steward', name='steward'),
    url(r'^manage/', include('manager.urls', namespace='manage')),
    url(r'^attendance/$', 'attendance.views.attendance', name='attendance'),

    # AJAX
    url(r'^ajax/create_weeks/$', 'attendance.views.createWeeks'),
    url(r'^ajax/get_week_group_attendance/$', 'attendance.views.getWeekGroupAttendance'),
    url(r'^ajax/change_attendance_hours/$', 'attendance.views.changeAttendanceHours'),
    url(r'^ajax/get_existing_weeks/$', 'attendance.views.getExistingWeeks'),
    url(r'^ajax/delete_weeks_by_id/$', 'attendance.views.deleteWeeksById'),
    url(r'^ajax/get_statistics/(?P<target>\w+)/$', 'attendance.views.getStatistics'),
    url(r'^ajax/search_accounts/$', 'accounts.views.searchAccounts'),
    url(r'^ajax/user_info/$', 'accounts.views.userInfo'),

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
