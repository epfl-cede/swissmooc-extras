# -*- coding: utf-8 -*-
# Generated by Django 4.1.10 on 2023-08-28 13:04
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('split_logs', '0027_alter_course_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursedump',
            name='is_encypted',
            field=models.BooleanField(default=True),
        ),
    ]
