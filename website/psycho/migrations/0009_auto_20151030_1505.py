# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('psycho', '0008_auto_20151028_0730'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='activity_type',
        ),
        migrations.RemoveField(
            model_name='response',
            name='created',
        ),
        migrations.AddField(
            model_name='response',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 30, 15, 5, 45, 738755, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='answerbase',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='useractivity',
            name='ended',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='useractivity',
            name='started',
            field=models.DateTimeField(editable=False),
        ),
    ]
