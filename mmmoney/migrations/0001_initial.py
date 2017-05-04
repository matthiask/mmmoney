# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-04 14:22
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Access',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'accesses',
                'verbose_name': 'access',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='client')),
            ],
            options={
                'verbose_name_plural': 'clients',
                'verbose_name': 'client',
            },
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=datetime.datetime.now, verbose_name='created')),
                ('date', models.DateField(default=datetime.date.today, verbose_name='date')),
                ('currency', models.CharField(choices=[(b'CHF', b'CHF')], default=b'CHF', max_length=3, verbose_name='currency')),
                ('total', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='total')),
                ('notes', models.CharField(max_length=200, verbose_name='notes')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mmmoney.Client', verbose_name='client')),
            ],
            options={
                'ordering': ['-date', '-created'],
                'verbose_name_plural': 'entries',
                'verbose_name': 'entry',
            },
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mmmoney.Client', verbose_name='client')),
            ],
            options={
                'ordering': ['ordering'],
                'verbose_name_plural': 'lists',
                'verbose_name': 'list',
            },
        ),
        migrations.AddField(
            model_name='entry',
            name='list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='mmmoney.List', verbose_name='list'),
        ),
        migrations.AddField(
            model_name='entry',
            name='paid_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to=settings.AUTH_USER_MODEL, verbose_name='paid by'),
        ),
        migrations.AddField(
            model_name='access',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mmmoney.Client', verbose_name='client'),
        ),
        migrations.AddField(
            model_name='access',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
