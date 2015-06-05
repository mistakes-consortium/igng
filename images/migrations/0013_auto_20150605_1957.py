# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0012_auto_20150605_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='user',
            field=models.ForeignKey(related_name='galleries', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='gallery',
            unique_together=set([('user', 'title')]),
        ),
    ]
