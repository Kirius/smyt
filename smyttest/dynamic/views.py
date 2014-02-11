# coding: utf-8
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.views.decorators.http import require_POST

from dynamic.models import dynamic_models, get_field_type
from dynamic.utils import json_response


def home(request):
    models = [{'name': name, 'verbose_name': model._meta.verbose_name}
                for name, model in dynamic_models.items()]

    return render(request, 'dynamic/main.html', {'models': models})


@json_response
def get_data(request):
    model_name = request.GET.get('model')
    model = dynamic_models[model_name]
    rows = [model_to_dict(row) for row in model.objects.all()]
    headers = {name: (model._meta.get_field(name).verbose_name,
                      get_field_type(model._meta.get_field(name)))
                for name in rows[0].keys()}
    del headers['id']
    return {'headers': headers, 'rows': rows}


@require_POST
@json_response
def update_data(request):
    model_name = request.POST['model']
    id = request.POST['id']
    field_name = request.POST['field']
    value = request.POST['value']

    model = dynamic_models[model_name]
    record = model.objects.get(id=id)
    if not hasattr(record, field_name):
        raise AttributeError

    setattr(record, field_name, value)
    record.save()
    return {'success': True}
