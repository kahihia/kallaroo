# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-11 17:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='contractor',
        ),
    ]
