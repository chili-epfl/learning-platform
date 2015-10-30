# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psycho', '0007_auto_20151028_0718'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='activity_one',
        ),
        migrations.RemoveField(
            model_name='user',
            name='activity_two',
        ),
    ]
