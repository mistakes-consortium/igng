# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0004_auto_20141207_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exifvalue',
            name='value',
            field=models.TextField(),
            preserve_default=True,
        ),
    ]
