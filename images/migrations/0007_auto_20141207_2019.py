# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0006_auto_20141207_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exifkey',
            name='key',
            field=models.CharField(max_length=64, null=True, blank=True),
            preserve_default=True,
        ),
    ]
