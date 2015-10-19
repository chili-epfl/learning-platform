# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psycho', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='user',
            field=models.ForeignKey(default=1, to='psycho.User'),
            preserve_default=False,
        ),
    ]
