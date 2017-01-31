# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import bitfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0015_auto_20160906_0102'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='view_default',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='image',
            name='view_flags',
            field=bitfield.models.BitField(((b'view_3d_180', b'180 Degrees 3D'), (b'view_3d_180', b'360 Degrees 3D'), (b'view_2d_pano', b'Panoramic')), default=None, null=True),
        ),
    ]
