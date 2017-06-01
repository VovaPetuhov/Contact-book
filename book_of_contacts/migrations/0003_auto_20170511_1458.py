# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-11 11:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book_of_contacts', '0002_auto_20170511_1329'),
    ]

    operations = [
        migrations.CreateModel(
            name='InContacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_to_contacts', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RenameField(
            model_name='contacts',
            old_name='name',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='contacts',
            old_name='surname',
            new_name='last_name',
        ),
        migrations.RemoveField(
            model_name='contacts',
            name='username',
        ),
        migrations.AddField(
            model_name='contacts',
            name='country',
            field=models.CharField(default=None, max_length=24),
        ),
        migrations.AddField(
            model_name='contacts',
            name='email',
            field=models.EmailField(default=None, max_length=254),
        ),
        migrations.AddField(
            model_name='contacts',
            name='phone_nmb',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name='contacts',
            name='town',
            field=models.CharField(default=None, max_length=24),
        ),
        migrations.AddField(
            model_name='incontacts',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_of_contacts.Contacts'),
        ),
        migrations.AddField(
            model_name='incontacts',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
