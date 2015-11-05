# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psycho', '0013_auto_20151105_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='source',
            field=models.URLField(),
        ),
    ]
