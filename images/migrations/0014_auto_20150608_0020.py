# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import images.models
import enumfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0013_auto_20150605_1957'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='display_density',
            field=enumfields.fields.EnumIntegerField(default=2, max_length=1, enum=images.models.Gallery.DisplaySize),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='rel_end',
            field=models.DateField(null=True, verbose_name=b'Time Period End', blank=True),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='rel_start',
            field=models.DateField(null=True, verbose_name=b'Time Period Start', blank=True),
        ),
    ]
