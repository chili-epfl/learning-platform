# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psycho', '0014_auto_20151105_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='source',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='test',
            name='category',
            field=models.CharField(max_length=20, choices=[(b'PRETEST', b'PreTest'), (b'PSYCHO', b'Psycho'), (b'ASSESS', b'Assess')]),
        ),
    ]
