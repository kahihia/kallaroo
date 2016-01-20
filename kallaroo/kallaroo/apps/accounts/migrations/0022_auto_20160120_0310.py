# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-20 03:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_auto_20160119_0358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='stripe_id',
        ),
        migrations.AddField(
            model_name='user',
            name='stripe_account_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='stripe_bank_account_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='stripe_card_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
