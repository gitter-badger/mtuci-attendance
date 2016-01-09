# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LastChange',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(verbose_name='Обновлено', auto_now=True)),
                ('commit', models.CharField(null=True, verbose_name='Первые 7 символов хэша коммита', blank=True, max_length=7)),
                ('changeDate', models.DateTimeField(null=True, verbose_name='Дата обновления', blank=True, default=datetime.datetime(2016, 1, 9, 11, 40, 11, 447765, tzinfo=utc))),
                ('description', models.TextField(null=True, verbose_name='Описание изменений', blank=True)),
            ],
            options={
                'get_latest_by': 'changeDate',
                'verbose_name': 'обновление',
                'verbose_name_plural': 'обновления',
                'ordering': ['-changeDate', '-created_at'],
            },
        ),
    ]
