# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psycho', '0010_auto_20151030_1511'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='link',
        ),
        migrations.AddField(
            model_name='activity',
            name='source',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
