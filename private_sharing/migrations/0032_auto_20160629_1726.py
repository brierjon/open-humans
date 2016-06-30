# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-29 17:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('private_sharing', '0031_auto_20160629_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='datarequestproject',
            name='returned_data_description',
            field=models.CharField(blank=True, max_length=140, verbose_name="A description of data you plan to upload back to the member's profile (140 characters max)"),
        ),
        migrations.AlterField(
            model_name='datarequestproject',
            name='active',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=True, help_text='"Active" status is required to perform authorization\nprocesses, including during drafting stage. If a project is not active, it\nwon\'t show up in listings of activities that can be joined by participants, and\nnew data sharing authorizations cannot occur. Projects which are "active" but\nnot approved may have some information shared in an "In Development" section,\nso Open Humans members can see potential upcoming studies. Removing "active"\nstatus from a project will not remove any uploaded files from a project\nmember\'s profile.'),
        ),
    ]
