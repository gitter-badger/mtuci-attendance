# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='is_complited',
            field=models.BooleanField(default=False, verbose_name='Выполнено?'),
        ),
    ]
