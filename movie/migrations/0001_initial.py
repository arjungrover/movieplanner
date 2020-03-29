# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2020-03-18 12:04
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MovieGenre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('genre', models.IntegerField(choices=[(1, 'Action'), (2, 'Adventure'), (3, 'Comedy'), (4, 'Crime'), (5, 'Drama'), (6, 'Historical')], verbose_name='Genre')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MovieInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Movie Name')),
                ('description', models.TextField(verbose_name='Movie Description')),
                ('run_time', models.TimeField(verbose_name='Movie Duration')),
                ('buffer', models.TimeField(verbose_name='Buffer Time')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ShowDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('start_time', models.TimeField(verbose_name='Show Start Time')),
                ('end_time', models.TimeField(verbose_name='Show End Time')),
                ('total_seats', models.PositiveIntegerField(default=0, verbose_name='Total Seats')),
                ('booked_seats', models.PositiveIntegerField(default=0, verbose_name='Booked Seats')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserMovie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.ShowDetail')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
