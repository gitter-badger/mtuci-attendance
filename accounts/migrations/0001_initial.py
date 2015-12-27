# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('username', models.CharField(unique=True, verbose_name='Логин', max_length=40)),
                ('first_name', models.CharField(blank=True, verbose_name='Имя', max_length=40, default='')),
                ('last_name', models.CharField(blank=True, verbose_name='Фамилия', max_length=40, default='')),
                ('patronymic', models.CharField(blank=True, verbose_name='Отчество', max_length=40, default='')),
                ('is_active', models.BooleanField(verbose_name='Активен?', default=True)),
                ('is_admin', models.BooleanField(verbose_name='', default=False)),
                ('is_steward', models.BooleanField(verbose_name='Староста', default=False)),
                ('is_deanery', models.BooleanField(verbose_name='Деканат', default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(verbose_name='Обновлен', auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'пользователи',
                'verbose_name': 'пользователь',
                'ordering': ['-created_at'],
                'get_latest_by': 'created_at',
            },
        ),
    ]
