# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-04 19:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0004_auto_20160104_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='written_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
