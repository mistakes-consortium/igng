# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import images.models
import enumfields.fields
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0014_auto_20150608_0020'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='display_sort',
            field=enumfields.fields.EnumIntegerField(default=0, enum=images.models.DisplaySort),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='display_density',
            field=enumfields.fields.EnumIntegerField(default=2, enum=images.models.DisplaySize),
        ),
        migrations.AlterField(
            model_name='image',
            name='exif_data',
            field=models.ManyToManyField(to='images.EXIFEntry', blank=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
    ]
