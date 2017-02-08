# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import bitfield.models
import taggit_autosuggest.managers


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0016_auto_20170131_1308'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='exif_timestamp',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='tags',
            field=taggit_autosuggest.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='image',
            name='view_flags',
            field=bitfield.models.BitField(((b'view_3d_180', b'180 Degrees 3D'), (b'view_3d_360', b'360 Degrees 3D'), (b'view_2d_pano', b'Panoramic')), default=None, null=True),
        ),
    ]
