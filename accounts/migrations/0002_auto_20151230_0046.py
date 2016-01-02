# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='universitygroup',
            name='created_at',
            field=models.DateTimeField(verbose_name='Создана', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='universitygroup',
            name='name',
            field=models.CharField(unique=True, default='', verbose_name='Название группы', max_length=15, blank=True),
        ),
        migrations.AlterField(
            model_name='universitygroup',
            name='updated_at',
            field=models.DateTimeField(verbose_name='Обновлена', auto_now=True),
        ),
        migrations.AlterUniqueTogether(
            name='account',
            unique_together=set([]),
        ),
    ]
