# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-24 20:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20151224_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractor',
            name='is_online',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_online',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='contractorprofile',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
