# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-09 17:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_auto_20160211_2024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraddress',
            name='zipcode',
        ),
        migrations.AddField(
            model_name='useraddress',
            name='postal_code',
            field=models.CharField(default=94011, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='street_number',
            field=models.CharField(max_length=10),
        ),
    ]
