# coding: utf-8
import datetime
import json
from django.http import HttpResponse


def json_handler(obj):
    if isinstance(obj, datetime.date):
        return obj.strftime('%Y-%m-%d')
    return json.dumps(obj)


def json_response(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        return HttpResponse(json.dumps(res, default=json_handler), content_type='application/json')

    return wrapper
