# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studyweek',
            name='semester',
            field=models.BooleanField(choices=[(False, 'Первый семестр'), (True, 'Второй семестр')], default=False, verbose_name='Номер семестра', help_text='Номер семестра в учебном году, не в календарном'),
        ),
    ]
