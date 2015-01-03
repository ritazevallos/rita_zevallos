# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table('blog_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('blog', ['Tag'])

        # Adding model 'Node'
        db.create_table('blog_node', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('private', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('external', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('locationX', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('locationY', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('locationZ', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('blog', ['Node'])

        # Adding M2M table for field tags on 'Node'
        m2m_table_name = db.shorten_name('blog_node_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('node', models.ForeignKey(orm['blog.node'], null=False)),
            ('tag', models.ForeignKey(orm['blog.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['node_id', 'tag_id'])

        # Adding model 'Link'
        db.create_table('blog_link', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_node', self.gf('django.db.models.fields.related.ForeignKey')(related_name='from', to=orm['blog.Node'])),
            ('to_node', self.gf('django.db.models.fields.related.ForeignKey')(related_name='to', to=orm['blog.Node'])),
        ))
        db.send_create_signal('blog', ['Link'])

        # Adding model 'Path'
        db.create_table('blog_path', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('blog', ['Path'])

        # Adding model 'PathNodeRelationship'
        db.create_table('blog_pathnoderelationship', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blog.Node'])),
            ('path', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blog.Path'])),
            ('order_index', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('blog', ['PathNodeRelationship'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table('blog_tag')

        # Deleting model 'Node'
        db.delete_table('blog_node')

        # Removing M2M table for field tags on 'Node'
        db.delete_table(db.shorten_name('blog_node_tags'))

        # Deleting model 'Link'
        db.delete_table('blog_link')

        # Deleting model 'Path'
        db.delete_table('blog_path')

        # Deleting model 'PathNodeRelationship'
        db.delete_table('blog_pathnoderelationship')


    models = {
        'blog.link': {
            'Meta': {'object_name': 'Link'},
            'from_node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from'", 'to': "orm['blog.Node']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to_node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to'", 'to': "orm['blog.Node']"})
        },
        'blog.node': {
            'Meta': {'object_name': 'Node'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'external': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'links': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_to+'", 'symmetrical': 'False', 'through': "orm['blog.Link']", 'to': "orm['blog.Node']"}),
            'locationX': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'locationY': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'locationZ': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'post_tags'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['blog.Tag']"}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'blog.path': {
            'Meta': {'object_name': 'Path'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nodes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'nodes'", 'symmetrical': 'False', 'through': "orm['blog.PathNodeRelationship']", 'to': "orm['blog.Node']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'blog.pathnoderelationship': {
            'Meta': {'object_name': 'PathNodeRelationship'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blog.Node']"}),
            'order_index': ('django.db.models.fields.IntegerField', [], {}),
            'path': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blog.Path']"})
        },
        'blog.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['blog']