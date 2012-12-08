# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'EmailTemplate.title'
        db.delete_column('references_emailtemplate', 'title')

        # Adding field 'EmailTemplate.name'
        db.add_column('references_emailtemplate', 'name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Adding field 'EmailTemplate.slug'
        db.add_column('references_emailtemplate', 'slug',
                      self.gf('django.db.models.fields.CharField')(default='-', max_length=255),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'EmailTemplate.title'
        raise RuntimeError("Cannot reverse this migration. 'EmailTemplate.title' and its values cannot be restored.")
        # Deleting field 'EmailTemplate.name'
        db.delete_column('references_emailtemplate', 'name')

        # Deleting field 'EmailTemplate.slug'
        db.delete_column('references_emailtemplate', 'slug')


    models = {
        'references.area': {
            'Meta': {'object_name': 'Area'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'areas'", 'to': "orm['references.State']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'references.emailtemplate': {
            'Meta': {'object_name': 'EmailTemplate'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'template': ('django.db.models.fields.TextField', [], {}),
            'template_html': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'references.level': {
            'Meta': {'ordering': "['order', 'title']", 'object_name': 'Level'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'references.qualification': {
            'Meta': {'ordering': "['order', 'title']", 'object_name': 'Qualification'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'references.state': {
            'Meta': {'object_name': 'State'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'references.subject': {
            'Meta': {'ordering': "['order', 'title']", 'object_name': 'Subject'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['references']