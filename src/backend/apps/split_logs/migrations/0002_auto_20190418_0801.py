# -*- coding: utf-8 -*-
# Generated by Django 2.2 on 2019-04-18 08:01
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('split_logs', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FilesSplitted',
            new_name='DirOriginal',
        ),
        migrations.CreateModel(
            name='FileOriginal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('dir_original', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='split_logs.DirOriginal')),
            ],
        ),
    ]
