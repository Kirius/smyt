# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'rooms'
        db.delete_table(u'dynamic_rooms')

        # Deleting model 'users'
        db.delete_table(u'dynamic_users')


    def backwards(self, orm):
        # Adding model 'rooms'
        db.create_table(u'dynamic_rooms', (
            ('department', self.gf('django.db.models.fields.CharField')(max_length=200)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('spots', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'dynamic', ['rooms'])

        # Adding model 'users'
        db.create_table(u'dynamic_users', (
            ('paycheck', self.gf('django.db.models.fields.IntegerField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('date_joined', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'dynamic', ['users'])


    models = {
        
    }

    complete_apps = ['dynamic']