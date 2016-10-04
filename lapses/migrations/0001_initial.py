# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import lapses.models
import django_extensions.db.fields
import enumfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0015_auto_20160906_0102'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoLapseConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', django_extensions.db.fields.ShortUUIDField(db_index=True, editable=False, name=b'uuid', blank=True)),
                ('create_new_every', models.IntegerField(help_text=b'How many uploads until we automatically generate a lapse')),
                ('image_count', models.IntegerField(help_text=b'How many images maximum to lapse')),
                ('frames_per_second', models.IntegerField(help_text=b'FPS of the resulting video')),
                ('enabled', models.BooleanField()),
                ('max_output_size', enumfields.fields.EnumIntegerField(help_text=b'Biggest size we generate', enum=lapses.models.AutoLapseOutputSizes)),
                ('source_gallery', models.ForeignKey(related_name='autolapse_configs', to='images.Gallery')),
            ],
        ),
        migrations.CreateModel(
            name='AutoLapseInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('uuid', django_extensions.db.fields.ShortUUIDField(db_index=True, editable=False, name=b'uuid', blank=True)),
                ('status', enumfields.fields.EnumIntegerField(enum=lapses.models.LapseInstanceStatus)),
                ('configuration', models.ForeignKey(related_name='autolapse_instances', to='lapses.AutoLapseConfiguration')),
            ],
            options={
                'get_latest_by': 'created',
            },
        ),
        migrations.CreateModel(
            name='AutoLapseInstanceFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', django_extensions.db.fields.ShortUUIDField(db_index=True, editable=False, name=b'uuid', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('output_size', enumfields.fields.EnumIntegerField(enum=lapses.models.AutoLapseOutputSizes)),
                ('file_video_mp4', models.FileField(max_length=512, upload_to=lapses.models.video_mp4_name_generator)),
                ('file_video_webm', models.FileField(max_length=512, upload_to=lapses.models.video_webm_name_generator)),
                ('file_video_gif', models.ImageField(max_length=512, upload_to=lapses.models.gif_name_generator)),
                ('instance', models.ForeignKey(related_name='autolapse_files', to='lapses.AutoLapseInstance')),
            ],
        ),
    ]
