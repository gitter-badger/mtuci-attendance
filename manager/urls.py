from django.conf.urls import patterns, url
from django.conf.urls import include
from manager import views

urlpatterns = patterns('',
    url(r'^$', views.main, name='main'),
    url(r'^schedule/$', views.schedule, name='schedule'),
    url(r'^users/$', views.users, name='users'),
)
