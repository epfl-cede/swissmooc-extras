# -*- coding: utf-8 -*-
# Generated by Django 2.2 on 2019-05-10 09:17
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('split_logs', '0017_auto_20190509_1223'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coursedump',
            old_name='is_dumped',
            new_name='is_dumped_mongo',
        ),
        migrations.RenameField(
            model_name='coursedump',
            old_name='is_encypted',
            new_name='is_dumped_mysql',
        ),
    ]
