# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=100)),
                ('age', models.IntegerField()),
                ('score_test', models.IntegerField(null=True)),
                ('score_pre', models.IntegerField(null=True)),
                ('score_post', models.IntegerField(null=True)),
            ],
        ),
    ]
