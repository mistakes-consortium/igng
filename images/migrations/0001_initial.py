# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields
from django.conf import settings
import taggit.managers
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FeaturedImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('rel_start', models.DateField(null=True, blank=True)),
                ('rel_end', models.DateField(null=True, blank=True)),
                ('title', models.CharField(max_length=256, null=True, blank=True)),
                ('private', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=256, null=True, blank=True)),
                ('uuid', django_extensions.db.fields.ShortUUIDField(max_length=12, editable=False, name=b'uuid', blank=True)),
                ('file', imagekit.models.fields.ProcessedImageField(upload_to=b'')),
                ('gallery', models.ForeignKey(to='images.Gallery')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='featuredimage',
            name='image',
            field=models.ForeignKey(to='images.Image'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='featuredimage',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
