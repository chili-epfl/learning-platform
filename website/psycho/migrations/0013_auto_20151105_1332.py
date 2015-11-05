# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psycho', '0012_auto_20151105_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='category',
            field=models.IntegerField(default=1, choices=[(1, b'first concept'), (2, b'second concept')]),
        ),
    ]
