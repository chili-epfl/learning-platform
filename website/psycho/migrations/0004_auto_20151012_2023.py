# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psycho', '0003_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerBase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('interview_uuid', models.CharField(max_length=36, verbose_name=b'Interview unique identifier')),
                ('test', models.ForeignKey(to='psycho.Test')),
            ],
        ),
        migrations.CreateModel(
            name='AnswerRadio',
            fields=[
                ('answerbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='psycho.AnswerBase')),
                ('body', models.TextField(null=True, blank=True)),
            ],
            bases=('psycho.answerbase',),
        ),
        migrations.CreateModel(
            name='AnswerText',
            fields=[
                ('answerbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='psycho.AnswerBase')),
                ('body', models.TextField(null=True, blank=True)),
            ],
            bases=('psycho.answerbase',),
        ),
        migrations.AddField(
            model_name='answerbase',
            name='question',
            field=models.ForeignKey(to='psycho.Question'),
        ),
        migrations.AddField(
            model_name='answerbase',
            name='response',
            field=models.ForeignKey(to='psycho.Response'),
        ),
    ]
