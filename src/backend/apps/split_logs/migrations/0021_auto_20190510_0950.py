# -*- coding: utf-8 -*-
# Generated by Django 2.2 on 2019-05-10 09:50
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('split_logs', '0020_coursedumptable_db_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coursedump',
            old_name='is_dumped_mongo',
            new_name='is_encypted',
        ),
        migrations.RemoveField(
            model_name='coursedump',
            name='is_dumped_mysql',
        ),
    ]
