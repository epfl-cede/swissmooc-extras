# -*- coding: utf-8 -*-
# Generated by Django 2.2 on 2019-05-10 09:40
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('split_logs', '0019_remove_coursedump_id_uploaded'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursedumptable',
            name='db_name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
