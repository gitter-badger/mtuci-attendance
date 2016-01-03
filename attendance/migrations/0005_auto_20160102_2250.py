# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_auto_20151228_1346'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='studyweek',
            options={'verbose_name': 'учебная неделя', 'verbose_name_plural': 'учебные недели', 'ordering': ['startStudyYear', 'semester', 'number'], 'get_latest_by': 'created_at'},
        ),
        migrations.AlterField(
            model_name='studyweek',
            name='semester',
            field=models.BooleanField(help_text='Номер семестра в учебном году, не в календарном', default=False, db_index=True, verbose_name='Номер семестра', choices=[(False, 'Первый семестр'), (True, 'Второй семестр')]),
        ),
        migrations.AlterField(
            model_name='studyweek',
            name='startStudyYear',
            field=models.PositiveSmallIntegerField(verbose_name='Год начала учебного года', validators=[django.core.validators.MinValueValidator(10, message='Минимальное значение 10'), django.core.validators.MaxValueValidator(35, message='Слишком большой номер года')], help_text='Две последние цифры в формате <em>YY</em>', db_index=True, default=16),
        ),
        migrations.AlterIndexTogether(
            name='attendance',
            index_together=set([('studyWeek', 'student')]),
        ),
        migrations.AlterIndexTogether(
            name='studyweek',
            index_together=set([('startStudyYear', 'semester', 'number'), ('startStudyYear', 'semester')]),
        ),
    ]
