# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import images.models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0007_auto_20141207_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='uuid',
            field=django_extensions.db.fields.ShortUUIDField(default='a', editable=False, name=b'uuid', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='image',
            name='original',
            field=models.ImageField(upload_to=images.models.set_image_name_on_upload),
            preserve_default=True,
        ),
    ]
