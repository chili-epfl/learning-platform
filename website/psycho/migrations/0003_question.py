# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psycho', '0002_test'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('question_type', models.CharField(default=b'text', max_length=200, choices=[(b'text', b'text'), (b'radio', b'radio')])),
                ('choices', models.TextField(help_text=b'if the question type is "radio," provide a comma-separated list of options for this question .', null=True, blank=True)),
                ('test', models.ForeignKey(to='psycho.Test')),
            ],
        ),
    ]
