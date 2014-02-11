# coding: utf-8
from django.contrib import admin
from dynamic.models import dynamic_models

# register all dynamically created models in admin
for name, obj in dynamic_models.items():
    admin.site.register(obj)
