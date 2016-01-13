# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20160109_1556'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(verbose_name='Обновлено', auto_now=True)),
                ('description', models.TextField(null=True, verbose_name='Описание пункта плана', blank=True, max_length=255)),
            ],
            options={
                'verbose_name_plural': 'планы',
                'verbose_name': 'план',
                'ordering': ['-created_at'],
                'get_latest_by': 'created_at',
            },
        ),
    ]
