# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20151230_0046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='first_name',
            field=models.CharField(verbose_name='Имя', default='', blank=True, max_length=40, db_index=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='last_name',
            field=models.CharField(verbose_name='Фамилия', default='', blank=True, max_length=40, db_index=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='patronymic',
            field=models.CharField(verbose_name='Отчество', default='', blank=True, max_length=40, db_index=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(verbose_name='Логин', unique=True, max_length=40, db_index=True),
        ),
    ]
