# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-26 13:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_auto_20180425_1513'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='user',
            new_name='users',
        ),
        migrations.AlterField(
            model_name='membership',
            name='status',
            field=models.IntegerField(choices=[(0, 'Requested'), (1, 'Unsubscribed'), (2, 'Joined'), (3, 'Admin')]),
        ),
    ]