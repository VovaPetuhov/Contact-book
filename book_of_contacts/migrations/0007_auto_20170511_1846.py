# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-11 15:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book_of_contacts', '0006_auto_20170511_1845'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='username',
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
    ]
