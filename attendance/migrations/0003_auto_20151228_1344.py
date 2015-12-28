# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
from django.utils.timezone import utc
import django.core.validators
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('attendance', '0002_studyweek_semester'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('numberOfHours', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(0, message='Не может быть меньше нуля'), django.core.validators.MaxValueValidator(250, message='Слишком большое число')], verbose_name='Номер в семестре')),
                ('created_at', models.DateTimeField(verbose_name='Создан', auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('student', models.ForeignKey(verbose_name='Студент', blank=True, help_text='Студент, который посещал занятия', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name_plural': 'посещения',
                'get_latest_by': 'created_at',
                'ordering': ['-studyWeek', '-created_at'],
                'verbose_name': 'посещение',
            },
        ),
        migrations.AddField(
            model_name='studyweek',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 28, 10, 44, 16, 308585, tzinfo=utc), verbose_name='Создан', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studyweek',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 28, 10, 44, 26, 224024, tzinfo=utc), auto_now=True, verbose_name='Обновлен'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='studyweek',
            name='number',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, message='Отсчёт начинается с единицы'), django.core.validators.MaxValueValidator(25, message='Слишком большой номер недели')], verbose_name='Номер в семестре'),
        ),
        migrations.AlterUniqueTogether(
            name='studyweek',
            unique_together=set([('startStudyYear', 'number', 'semester')]),
        ),
        migrations.AddField(
            model_name='attendance',
            name='studyWeek',
            field=models.ForeignKey(verbose_name='Неделя', blank=True, help_text='Учебная неделя, для которой указывается посещение', to='attendance.StudyWeek', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together=set([('student', 'studyWeek')]),
        ),
    ]
