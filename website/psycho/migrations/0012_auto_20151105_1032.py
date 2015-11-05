# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psycho', '0011_auto_20151105_1012'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='category',
            field=models.CharField(default=1, max_length=100, choices=[(1, b'first concept'), (2, b'second concept')]),
        ),
        migrations.AlterField(
            model_name='activity',
            name='source',
            field=models.CharField(max_length=200),
        ),
    ]
