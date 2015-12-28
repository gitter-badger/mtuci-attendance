# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0003_auto_20151228_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='numberOfHours',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0, message='Не может быть меньше нуля'), django.core.validators.MaxValueValidator(250, message='Слишком большое число')], verbose_name='Количество часов', default=0),
        ),
    ]
