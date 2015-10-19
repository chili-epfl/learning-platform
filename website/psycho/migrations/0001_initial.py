# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
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
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('question_type', models.CharField(default=b'text', max_length=200, choices=[(b'text', b'text'), (b'radio', b'radio')])),
                ('choices', models.TextField(help_text=b'if the question type is "radio," provide a comma-separated list of options for this question .', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('interview_uuid', models.CharField(max_length=36, verbose_name=b'Interview unique identifier')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('category', models.CharField(max_length=20, choices=[(b'PRETEST', b'PreTest'), (b'PSYCHO', b'Psycho')])),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(unique=True, max_length=100)),
                ('age', models.IntegerField()),
                ('score_test', models.IntegerField(null=True)),
                ('score_pre', models.IntegerField(null=True)),
                ('score_post', models.IntegerField(null=True)),
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
            model_name='response',
            name='test',
            field=models.ForeignKey(to='psycho.Test'),
        ),
        migrations.AddField(
            model_name='question',
            name='test',
            field=models.ForeignKey(to='psycho.Test'),
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
