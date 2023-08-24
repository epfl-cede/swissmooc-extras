# -*- coding: utf-8 -*-
# Generated by Django 2.2 on 2019-05-02 12:22
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('split_logs', '0010_auto_20190501_1201'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseDump',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('is_dumped', models.CharField(choices=[('0', 'no'), ('1', 'yes')], default='0', max_length=1)),
                ('is_encypted', models.CharField(choices=[('0', 'no'), ('1', 'yes')], default='0', max_length=1)),
                ('id_uploaded', models.CharField(choices=[('0', 'no'), ('1', 'yes')], default='0', max_length=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='split_logs.Course')),
            ],
            options={
                'unique_together': {('course', 'date')},
            },
        ),
    ]