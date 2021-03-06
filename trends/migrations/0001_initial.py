# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-18 20:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Backlink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('predicate', models.CharField(max_length=255)),
                ('count', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Endpoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uri', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uri', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='backlink',
            name='endpoint',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trends.Endpoint'),
        ),
        migrations.AddField(
            model_name='backlink',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trends.Resource'),
        ),
    ]
