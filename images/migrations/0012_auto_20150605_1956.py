# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0011_auto_20150605_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='deletable',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='private',
            field=models.BooleanField(default=True),
        ),
    ]
