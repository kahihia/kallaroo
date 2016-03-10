# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-11 17:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0014_auto_20160111_1741'),
        ('chats', '0006_auto_20160111_1741'),
        ('reviews', '0004_auto_20160111_1741'),
        ('notifications', '0002_remove_notification_contractor'),
        ('accounts', '0015_auto_20160108_0541'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contractorprofile',
            name='contractor',
        ),
        migrations.RemoveField(
            model_name='contractorprofile',
            name='subcategory',
        ),
        migrations.DeleteModel(
            name='Contractor',
        ),
        migrations.DeleteModel(
            name='ContractorProfile',
        ),
    ]
