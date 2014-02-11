# coding: utf-8
from django.conf.urls import patterns, url


urlpatterns = patterns(
    'dynamic.views',
    url(r'^api/get$', 'get_data', name='get_data'),
    url(r'^api/update$', 'update_data', name='update_data'),
    url(r'^api/insert$', 'insert_data', name='insert_data'),
)
