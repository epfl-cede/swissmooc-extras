# -*- coding: utf-8 -*-
# Generated by Django 2.2 on 2019-04-18 08:01
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('split_logs', '0002_auto_20190418_0801'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='fileoriginal',
            unique_together={('name', 'dir_original')},
        ),
    ]
