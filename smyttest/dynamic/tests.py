# coding: utf-8

from django.test import TestCase
from django.db.models.base import ModelBase
import datetime

import dynamic.models as dm


class DynamicModelsTests(TestCase):

    def test_models_creation(self):
        '''
        check if models are created
        and that they are of correct type.
        '''
        self.assertTrue(hasattr(dm, 'Rooms'))
        self.assertTrue(hasattr(dm, 'Articles'))
        self.assertTrue(isinstance(dm.Articles, ModelBase))
        self.assertTrue(isinstance(dm.Rooms, ModelBase))

    def test_model_instances_creation(self):
        '''
        check that instances of dynamic models are created properly.
        '''
        self.assertEqual(dm.Rooms.objects.count(), 0)
        dm.Rooms.objects.create(department='My department', spots=100)
        self.assertEqual(dm.Rooms.objects.count(), 1)
        room = dm.Rooms.objects.all()[0]
        self.assertTrue(hasattr(room, 'department'))
        self.assertTrue(hasattr(room, 'spots'))
        self.assertEqual(room.department, 'My department')
        self.assertEqual(room.spots, 100)

        self.assertEqual(dm.Articles.objects.count(), 0)
        date = datetime.date(2014, 02, 10)
        article = dm.Articles.objects.create(
            title='My article', text='My text', date_published=date)
        self.assertEqual(dm.Articles.objects.count(), 1)
        self.assertTrue(hasattr(article, 'title'))
        self.assertTrue(hasattr(article, 'text'))
        self.assertTrue(hasattr(article, 'date_published'))
        self.assertEqual(article.title, 'My article')
        self.assertEqual(article.text, 'My text')
        self.assertEqual(article.date_published, date)
