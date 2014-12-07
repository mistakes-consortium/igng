# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0003_auto_20141207_1907'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='file',
        ),
        migrations.AddField(
            model_name='image',
            name='original',
            field=models.ImageField(default=1, upload_to=b'uploads'),
            preserve_default=False,
        ),
    ]
