# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0005_auto_20160102_2250'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attendance',
            options={'get_latest_by': 'created_at', 'verbose_name': 'посещение', 'verbose_name_plural': 'посещения', 'ordering': ['studyWeek', '-created_at']},
        ),
    ]
