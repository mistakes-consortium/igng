# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0008_auto_20141207_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='uuid',
            field=django_extensions.db.fields.ShortUUIDField(db_index=True, editable=False, name=b'uuid', blank=True),
            preserve_default=True,
        ),
    ]
