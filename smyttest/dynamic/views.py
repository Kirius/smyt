from django.shortcuts import render

from dynamic.models import dynamic_models


def home(request):
    models = [{'name': name, 'verbose_name': model._meta.verbose_name}
                for name, model in dynamic_models.items()]
    context = {
        'models': models,
    }
    return render(request, 'dynamic/main.html', context)
