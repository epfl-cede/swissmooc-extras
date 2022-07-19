# -*- coding: utf-8 -*-
# Generated by Django 2.2 on 2019-05-09 09:08
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('check_ssl', '0010_auto_20190412_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='error',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='hostname',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
