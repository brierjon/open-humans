# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-22 16:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_import', '0004_auto_20160822_1618'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datafile',
            name='is_latest',
        ),
    ]
