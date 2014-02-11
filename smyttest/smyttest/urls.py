# coding: utf-8
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'dynamic.views.home', name='home'),
    url(r'^dynamic/', include('dynamic.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
