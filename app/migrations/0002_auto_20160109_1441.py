# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lastchange',
            name='changeDate',
            field=models.DateTimeField(null=True, default=django.utils.timezone.now, verbose_name='Дата обновления', blank=True),
        ),
    ]
