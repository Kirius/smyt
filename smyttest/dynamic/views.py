# coding: utf-8
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.views.decorators.http import require_POST
from django.forms import ValidationError
from django.db import IntegrityError

from dynamic.models import dynamic_models, get_field_type
from dynamic.utils import json_response


def home(request):
    '''
    Main page
    '''
    models = [{'name': name, 'verbose_name': model._meta.verbose_name}
              for name, model in dynamic_models.items()]

    return render(request, 'dynamic/main.html', {'models': models})


@json_response
def get_data(request):
    '''
    Returns json data for requested dynamic model.
    Used in AJAX call.
    '''
    model_name = request.GET.get('model')
    try:
        model = dynamic_models[model_name]
    except KeyError:
        return {'success': False}
    rows = [model_to_dict(row) for row in model.objects.all()]
    headers = {name: (model._meta.get_field(name).verbose_name,
                      get_field_type(model._meta.get_field(name)))
               for name in model._meta.get_all_field_names()}
    del headers['id']
    return {'success': True, 'headers': headers, 'rows': rows}


@require_POST
@json_response
def update_data(request):
    '''
    Updates given field of a given record of a given dynamic model.
    Used in AJAX call.
    '''
    model_name = request.POST.get('model')
    id = request.POST.get('id')
    field_name = request.POST.get('field')
    value = request.POST.get('value')

    try:
        model = dynamic_models[model_name]
    except KeyError:
        return {'success': False}

    try:
        record = model.objects.get(id=id)
    except model.DoesNotExist:
        return {'success': False}

    if not hasattr(record, field_name):
        return {'success': False}

    try:
        setattr(record, field_name, value)
        record.save()
    except ValueError:
        return {'success': False}

    return {'success': True}


@require_POST
@json_response
def insert_data(request):
    '''
    Inserts new record to a given dynamic model.
    Used in AJAX call.
    '''
    data = {key: request.POST[key] for key in request.POST}
    try:
        model_name = data.pop('model')
        model = dynamic_models[model_name]
    except KeyError:
        return {'success': False}

    try:
        model.objects.create(**data)
    except (ValidationError, TypeError, IntegrityError):
        return {'success': False}

    return {'success': True}
