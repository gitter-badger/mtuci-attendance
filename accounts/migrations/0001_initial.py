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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('username', models.CharField(max_length=40, verbose_name='Логин', unique=True)),
                ('first_name', models.CharField(max_length=40, verbose_name='Имя', blank=True, default='')),
                ('last_name', models.CharField(max_length=40, verbose_name='Фамилия', blank=True, default='')),
                ('patronymic', models.CharField(max_length=40, verbose_name='Отчество', blank=True, default='')),
                ('is_active', models.BooleanField(verbose_name='Активен?', default=True)),
                ('is_admin', models.BooleanField(verbose_name='', default=False)),
                ('is_steward', models.BooleanField(verbose_name='Староста', default=False)),
                ('is_deanery', models.BooleanField(verbose_name='Деканат', default=False)),
                ('created_at', models.DateTimeField(verbose_name='Создан', auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
            ],
            options={
                'verbose_name': 'пользователь',
                'verbose_name_plural': 'пользователи',
                'get_latest_by': 'created_at',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='UniversityGroup',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=15, default='', verbose_name='Название', blank=True, unique=True)),
                ('created_at', models.DateTimeField(verbose_name='Создан', auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
            ],
            options={
                'verbose_name': 'группа студентов',
                'verbose_name_plural': 'группы студентов',
                'get_latest_by': 'created_at',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='account',
            name='universityGroup',
            field=models.ForeignKey(to='accounts.UniversityGroup', blank=True, null=True, verbose_name='Группа студента'),
        ),
        migrations.AlterUniqueTogether(
            name='account',
            unique_together=set([('is_steward', 'universityGroup')]),
        ),
    ]
