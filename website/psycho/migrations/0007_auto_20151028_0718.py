# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psycho', '0006_auto_20151020_1332'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserActivity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('started', models.DateTimeField(auto_now_add=True)),
                ('ended', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='activity',
            name='activity_type',
            field=models.CharField(default=b'Definition', max_length=100, choices=[(b'Definition', b'Definition'), (b'Example', b'EXAMPLE')]),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(default=b'text', max_length=100, choices=[(b'text', b'text'), (b'radio', b'radio')]),
        ),
        migrations.AddField(
            model_name='useractivity',
            name='activity',
            field=models.ForeignKey(to='psycho.Activity'),
        ),
        migrations.AddField(
            model_name='useractivity',
            name='user',
            field=models.ForeignKey(to='psycho.User'),
        ),
    ]
