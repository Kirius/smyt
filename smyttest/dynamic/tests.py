# coding: utf-8
from django.test import TestCase
from django.db.models.base import ModelBase
from django.core.urlresolvers import reverse
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


class DynamicViewsTests(TestCase):

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dynamic/main.html')

    def test_get_data_view_on_empty_db(self):
        '''
        Test that only headers are returned for a given model
        if no data in db for that model
        '''
        response = self.client.get(reverse('get_data'), {'model': 'Rooms'},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"success": true')
        self.assertContains(response, '"rows": []')
        self.assertContains(response, 'department')
        self.assertContains(response, 'spots')

        response = self.client.get(reverse('get_data'), {'model': 'Articles'},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"success": true')
        self.assertContains(response, '"rows": []')
        self.assertContains(response, 'title')
        self.assertContains(response, 'text')
        self.assertContains(response, 'date_published')

    def test_get_data_view_with_data(self):
        '''
        Test that correct data is returned for a given model
        when db has data for that model
        '''
        dm.Rooms.objects.create(department='My department', spots=100)
        response = self.client.get(reverse('get_data'), {'model': 'Rooms'},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"department": "My department"')
        self.assertContains(response, '"spots": 100')

        dm.Articles.objects.create(title='My article', text='My text',
                                   date_published=datetime.date(2014, 02, 10))
        response = self.client.get(reverse('get_data'), {'model': 'Articles'},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"title": "My article"')
        self.assertContains(response, '"text": "My text"')
        self.assertContains(response, '"date_published": "2014-02-10"')

    def test_get_data_view_unknown_model(self):
        '''
        Test view with non existing model
        '''
        response = self.client.get(reverse('get_data'), {'model': 'BAD_MODEL'},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"success": false')

    def test_update_data_view_on_non_existing_id(self):
        '''
        Try to update existing model, but not existing record
        '''
        response = self.client.post(
            reverse('update_data'),
            {'model': 'Rooms',
             'id': 1,
             'field': 'spots',
             'value': 'test'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"success": false')

    def test_update_data_view_with_wrong_field(self):
        '''
        Try to update existing model, existing record,
        but not existing field
        '''
        dm.Rooms.objects.create(id=1, department='My department', spots=100)
        response = self.client.post(
            reverse('update_data'),
            {'model': 'Rooms',
             'id': 1,
             'field': 'BAD_FIELD',
             'value': 'test'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"success": false')

    def test_update_data_view_unknown_model(self):
        '''
        Try to update not existing model
        '''
        dm.Rooms.objects.create(id=1, department='My department', spots=100)
        response = self.client.post(
            reverse('update_data'),
            {'model': 'UNKNOWN_MODEL',
             'id': 1,
             'field': 'spots',
             'value': 100},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"success": false')

    def test_update_data_view_wrong_type(self):
        '''
        Try to update model with wrong data type
        '''
        dm.Rooms.objects.create(id=1, department='My department', spots=100)
        response = self.client.post(
            reverse('update_data'),
            {'model': 'Rooms',
             'id': 1,
             'field': 'spots',
             'value': 'NOT A NUMBER'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"success": false')

    def test_update_data_view_correct(self):
        '''
        Try to update with all data correct
        '''
        dm.Rooms.objects.create(id=1, department='My department', spots=100)
        response = self.client.post(
            reverse('update_data'),
            {'model': 'Rooms',
             'id': 1,
             'field': 'spots',
             'value': 200},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"success": true')
        # check that created value updated in db
        self.assertEqual(dm.Rooms.objects.get(id=1).spots, 200)

    def test_insert_data_view_correct(self):
        '''
        Insert correct record in db
        '''
        response = self.client.post(
            reverse('insert_data'),
            {'model': 'Articles',
             'title': 'unique title',
             'text': 'My text',
             'date_published': '2013-12-04'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"success": true')
        self.assertEqual(dm.Articles.objects.get(title='unique title').text, 'My text')

    def test_insert_data_view_wrong_type(self):
        '''
        Insert record with incorrect field type
        '''
        response = self.client.post(
            reverse('insert_data'),
            {'model': 'Articles',
             'title': 'unique title',
             'text': 'My text',
             'date_published': 'NOT A DATE'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"success": false')

    def test_insert_data_view_unknown_model(self):
        '''
        Try to insert record into non existing model
        '''
        response = self.client.post(
            reverse('insert_data'),
            {'model': 'UNKNOWN_MODEL',
             'title': 'unique title',
             'text': 'My text',
             'date_published': 'NOT A DATE'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"success": false')

    def test_insert_data_view_with_wrong_field(self):
        '''
        Try to insert record with wrong field names
        '''
        response = self.client.post(
            reverse('insert_data'),
            {'model': 'Articles',
             'title': 'unique title',
             'text': 'My text',
             'date_published': '2012-05-12',
             'BAD_FIELD': 10},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"success": false')

    def test_insert_data_view_on_existing_id(self):
        '''
        Try to insert record with with ID that already exists in db
        '''
        dm.Articles.objects.create(id=1, title='t1', text='t1', date_published='2012-04-12')
        response = self.client.post(
            reverse('insert_data'),
            {'model': 'Articles',
             'title': 'unique title',
             'text': 'My text',
             'date_published': '2012-05-12',
             'id': 1
             },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"success": false')
