# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-22 22:26
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airline',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=100)),
                ('firstname', models.CharField(max_length=200)),
                ('lastname', models.CharField(max_length=200)),
                ('phonenumber', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
            ],
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('airport_id', models.CharField(max_length=5, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(message="Flight id must be entered in the format: '10000'. A 5 digit number not starting with 0.", regex='^[1-9]\\d{4,4}$')])),
                ('airport_name', models.CharField(max_length=20)),
                ('airport_country', models.CharField(max_length=20)),
                ('airport_city', models.CharField(max_length=20)),
                ('airport_news', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('flight_id', models.CharField(max_length=10, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(message="Flight id must be entered in the format: '1000000000'. A 10 digit number not starting with 0.", regex='^[1-9]\\d{9,9}$')])),
                ('business_classfare', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="Valid Price must be entered in the format: '5000.05 or 5000'.", regex='^\\d+(\\.\\d{1,2})?$')])),
                ('economy_classfare', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="Valid Price must be entered in the format: '5000.05 or 5000'.", regex='^\\d+(\\.\\d{1,2})?$')])),
                ('total_seats', models.CharField(max_length=4, validators=[django.core.validators.RegexValidator(message='Enter valid number of seats', regex='^\\d+$')])),
                ('daysoffset', models.CharField(max_length=1, validators=[django.core.validators.RegexValidator(message='Enter valid offset', regex='^\\d$')])),
                ('departure_time', models.CharField(max_length=8, validators=[django.core.validators.RegexValidator(message='Enter valid time of format HH:MM AM/PM 12hour', regex='^((1[0-2]|0?[1-9]):([0-5][0-9]) ([AaPp][Mm]))$')])),
                ('arrival_time', models.CharField(max_length=8, validators=[django.core.validators.RegexValidator(message='Enter valid time of format HH:MM AM/PM 12hour', regex='^((1[0-2]|0?[1-9]):([0-5][0-9]) ([AaPp][Mm]))$')])),
                ('airline_email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='air_rsv.Airline')),
                ('departureid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destinationid', to='air_rsv.Airport')),
                ('sourceid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sourceid', to='air_rsv.Airport')),
            ],
        ),
        migrations.CreateModel(
            name='Flight_instance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_departure', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Enter valid date', regex='^\\s*(3[01]|[12][0-9]|0?[1-9])\\.(1[012]|0?[1-9])\\.((?:19|20)\\d{2})\\s*$')])),
                ('available_seats', models.CharField(max_length=4, validators=[django.core.validators.RegexValidator(message='Enter valid number of seats', regex='^\\d+$')])),
                ('flight_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='air_rsv.Flight')),
            ],
        ),
        migrations.CreateModel(
            name='IntermediateStop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('daysoffset', models.CharField(max_length=1, validators=[django.core.validators.RegexValidator(message='Enter valid offset', regex='^\\d$')])),
                ('departure_time', models.CharField(max_length=8, validators=[django.core.validators.RegexValidator(message='Enter valid time of format HH:MM 24hour', regex='^((1[0-2]|0?[1-9]):([0-5][0-9]) ([AaPp][Mm]))$')])),
                ('arrival_time', models.CharField(max_length=8, validators=[django.core.validators.RegexValidator(message='Enter valid time of format HH:MM 24hour', regex='^((1[0-2]|0?[1-9]):([0-5][0-9]) ([AaPp][Mm]))$')])),
                ('flight_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='air_rsv.Flight')),
                ('stop_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='air_rsv.Airport')),
            ],
        ),
        migrations.CreateModel(
            name='Offers',
            fields=[
                ('offer_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('startdate', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Enter valid date', regex='^\\s*(3[01]|[12][0-9]|0?[1-9])\\.(1[012]|0?[1-9])\\.((?:19|20)\\d{2})\\s*$')])),
                ('end_date', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Enter valid date', regex='^\\s*(3[01]|[12][0-9]|0?[1-9])\\.(1[012]|0?[1-9])\\.((?:19|20)\\d{2})\\s*$')])),
                ('description', models.TextField(blank=True, null=True)),
                ('flight_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='air_rsv.Flight')),
            ],
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=100)),
                ('firstname', models.CharField(max_length=200)),
                ('lastname', models.CharField(max_length=200)),
                ('phonenumber', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(code='invalid_phonenumber', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
            ],
        ),
        migrations.CreateModel(
            name='RelevantAirports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('airport_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='air_rsv.Airport')),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='air_rsv.Passenger')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticket_id', models.CharField(max_length=10, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(message="Ticket id must be entered in the format: '1000000000'. A 10 digit number not starting with 0.", regex='^[1-9]\\d{9,9}$')])),
                ('date_of_departure', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Enter valid date', regex='^\\s*(3[01]|[12][0-9]|0?[1-9])\\.(1[012]|0?[1-9])\\.((?:19|20)\\d{2})\\s*$')])),
                ('flight_class', models.CharField(default='', max_length=10)),
                ('rating', models.CharField(default='', max_length=1)),
                ('status', models.CharField(default='', max_length=10, validators=[django.core.validators.RegexValidator(regex='^Booked|Waiting$')])),
                ('flight_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='air_rsv.Flight')),
                ('passenger_email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='air_rsv.Passenger')),
            ],
        ),
    ]
