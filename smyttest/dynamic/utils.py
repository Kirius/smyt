# coding: utf-8
import datetime
import json
from django.http import HttpResponse


def json_handler(obj):
    '''
    Allows to serialize datetime.date objects.
    '''
    if isinstance(obj, datetime.date):
        return obj.strftime('%Y-%m-%d')
    return json.dumps(obj)


def json_response(func):
    '''
    Decorator for responding json data.
    After applying to view function we can return
    plain python dictionary from view.
    '''
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        return HttpResponse(json.dumps(res, default=json_handler), content_type='application/json')

    return wrapper
