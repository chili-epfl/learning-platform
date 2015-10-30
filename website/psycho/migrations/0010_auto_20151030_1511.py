# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('psycho', '0009_auto_20151030_1505'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useractivity',
            name='ended',
        ),
        migrations.RemoveField(
            model_name='useractivity',
            name='started',
        ),
        migrations.AddField(
            model_name='useractivity',
            name='completed',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 30, 15, 11, 12, 667083, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
