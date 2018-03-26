# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-26 13:59
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('air_rsv', '0003_auto_20180326_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airline',
            name='phonenumber',
            field=models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message='Phone number incorrect format', regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.AlterField(
            model_name='offers',
            name='discount',
            field=models.CharField(default='0', max_length=2),
        ),
        migrations.AlterField(
            model_name='passenger',
            name='phonenumber',
            field=models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(code='invalid_phonenumber', message='Phone number incorrect format', regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
