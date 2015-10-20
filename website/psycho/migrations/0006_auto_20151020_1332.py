# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psycho', '0005_auto_20151018_1608'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='response',
            name='interview_uuid',
        ),
        migrations.RemoveField(
            model_name='user',
            name='score_post',
        ),
        migrations.RemoveField(
            model_name='user',
            name='score_pre',
        ),
    ]
