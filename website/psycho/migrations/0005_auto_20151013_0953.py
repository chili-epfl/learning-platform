# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psycho', '0004_auto_20151012_2023'),
    ]

    operations = [
        migrations.RenameField(
            model_name='test',
            old_name='type',
            new_name='category',
        ),
    ]
