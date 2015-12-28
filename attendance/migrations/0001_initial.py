# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StudyWeek',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('startStudyYear', models.PositiveSmallIntegerField(help_text='Две последние цифры в формате <em>YY</em>', verbose_name='Год начала учебного года', validators=[django.core.validators.MinValueValidator(10, message='Минимальное значение 10'), django.core.validators.MaxValueValidator(35, message='Слишком большой номер года')], default=15)),
                ('number', models.PositiveSmallIntegerField(verbose_name='Номер в семестре', validators=[django.core.validators.MinValueValidator(1, message='Отсчёт начинается с нуля'), django.core.validators.MaxValueValidator(25, message='Слишком большой номер недели')], default=1)),
            ],
            options={
                'verbose_name': 'учебная неделя',
                'verbose_name_plural': 'учебные недели',
                'ordering': ['startStudyYear', 'number'],
                'get_latest_by': 'created_at',
            },
        ),
    ]
