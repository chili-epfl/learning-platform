# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psycho', '0003_activity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='score_test',
        ),
    ]
