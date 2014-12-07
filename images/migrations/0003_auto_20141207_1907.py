# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_auto_20141201_0515'),
    ]

    operations = [
        migrations.CreateModel(
            name='EXIFEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExifKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExifValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='exifentry',
            name='key',
            field=models.ForeignKey(to='images.ExifKey'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='exifentry',
            name='value',
            field=models.ForeignKey(to='images.ExifValue'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='image',
            name='exif_data',
            field=models.ManyToManyField(to='images.EXIFEntry', null=True, blank=True),
            preserve_default=True,
        ),
    ]
