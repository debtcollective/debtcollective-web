# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DTRUserProfile'
        db.create_table(u'arcs_dtruserprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data', self.gf('jsonfield.fields.JSONField')()),
        ))
        db.send_create_signal(u'arcs', ['DTRUserProfile'])


    def backwards(self, orm):
        # Deleting model 'DTRUserProfile'
        db.delete_table(u'arcs_dtruserprofile')


    models = {
        u'arcs.dtruserprofile': {
            'Meta': {'object_name': 'DTRUserProfile'},
            'data': ('jsonfield.fields.JSONField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['arcs']