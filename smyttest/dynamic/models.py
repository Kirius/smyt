# coding: utf-8

from django.db import models
from django.conf import settings

import yaml

dynamic_models = {}


def get_field(field_type, title):
    """
    Returns django field based on field_type.
    Only char, int and date are supported
    """
    if field_type == 'char':
        return models.CharField(max_length=200, verbose_name=title)
    if field_type == 'date':
        return models.DateField(verbose_name=title)
    # Default is IntegerField
    return models.IntegerField(verbose_name=title)


def define_models():
    """
    Dynamically define django models based on yaml file.
    """
    tables = yaml.load(open(settings.YAML_FILENAME, 'rb'))

    if not tables:
        return

    for model_name in tables:
        attrs = {field['id'].lower(): get_field(field['type'], field['title'])
                    for field in tables[model_name]['fields']}

        attrs['__module__'] = __name__
        verbose_name = tables[model_name]['title']
        attrs['Meta'] = type(
            'Meta',
            tuple(),
            {'verbose_name': verbose_name,
             'verbose_name_plural': verbose_name}
        )
        capitalized_name = model_name.capitalize()
        new_model = type(
            capitalized_name,
            (models.Model, ),
            attrs
        )
        globals()[capitalized_name] = new_model
        dynamic_models[capitalized_name] = new_model

define_models()

# print rooms._meta.get_field('spots').verbose_name
# print rooms._meta.verbose_name
