# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-20 10:58
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('air_rsv', '0002_auto_20180320_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passenger',
            name='phonenumber',
            field=models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(code='invalid_phonenumber', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]