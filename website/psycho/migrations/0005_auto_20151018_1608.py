# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psycho', '0004_remove_user_score_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='activity_one',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='activity_two',
            field=models.IntegerField(null=True),
        ),
    ]
