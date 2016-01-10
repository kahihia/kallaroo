# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-05 20:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0011_auto_20160101_2208'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='final_payment',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=999, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='lng',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='task_clock_in',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='task_clock_out',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
