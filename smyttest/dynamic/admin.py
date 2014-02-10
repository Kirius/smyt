# coding: utf-8

from django.contrib import admin
from django.db.models.base import ModelBase
import dynamic.models

# register all dynamically created models in admin
for name, obj in dynamic.models.__dict__.iteritems():
    if isinstance(obj, ModelBase):
        admin.site.register(obj)
