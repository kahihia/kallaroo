# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-01 22:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_auto_20160101_2029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='ratings',
        ),
        migrations.RemoveField(
            model_name='task',
            name='reviews',
        ),
    ]