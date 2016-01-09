# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20160109_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lastchange',
            name='description',
            field=models.TextField(null=True, verbose_name='Описание изменений', blank=True, max_length=255),
        ),
    ]
