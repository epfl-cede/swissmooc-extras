# -*- coding: utf-8 -*-
# Generated by Django 2.2 on 2019-05-10 09:18
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('split_logs', '0018_auto_20190510_0917'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursedump',
            name='id_uploaded',
        ),
    ]
