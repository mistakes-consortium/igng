# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0005_auto_20141207_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='uuid',
            field=django_extensions.db.fields.ShortUUIDField(editable=False, name=b'uuid', blank=True),
            preserve_default=True,
        ),
    ]
