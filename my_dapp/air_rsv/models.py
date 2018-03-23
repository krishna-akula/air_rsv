# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models
from django.core.validators import RegexValidator
import hashlib
from django.core.validators import  *
from django.core.exceptions import ValidationError
import datetime
from .models import *
# Create your models here.

class Passenger(models.Model):
    # username = models.CharField(primary_key=True,max_length =50)
	email = models.EmailField(primary_key = True)
	password = models.CharField(max_length=100)
	firstname = models.CharField(max_length=200)
	lastname = models.CharField(max_length=200)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
                                 code='invalid_phonenumber') #############look into regex
	phonenumber = models.CharField(validators=[phone_regex],max_length=15,blank = True)
	def make_password(self ,password):
		assert password
		hashedpassword = hashlib.md5(password).hexdigest()
		return hashedpassword
	def check_password(self, password):
		assert password
		hashed = hashlib.md5(password).hexdigest()
		return self.password == hashed
	def set_password(self, password):
		self.password = password
	@property
	def name(self):
		return firstname + " " + lastname

class Airline(models.Model):
    # username = models.CharField(primary_key=True,max_length =50)
	email = models.EmailField(primary_key = True)
	password = models.CharField(max_length=100)
	firstname = models.CharField(max_length=200)
	lastname = models.CharField(max_length=200)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.") #############look into regex
	phonenumber = models.CharField(validators=[phone_regex],max_length=15,blank = True)
	def make_password(self ,password):
		assert password
		hashedpassword = hashlib.md5(password).hexdigest()
		return hashedpassword
	def check_password(self, password):
		assert password
		hashed = hashlib.md5(password).hexdigest()
		return self.password == hashed
	def set_password(self, password):
		self.password = password
	@property
	def name(self):
		return firstname + " " + lastname

class Airport(models.Model):
	airport_regex = RegexValidator(regex=r'^[1-9]\d{4,4}$', message="Flight id must be entered in the format: '10000'. A 5 digit number not starting with 0.")
	airport_id = models.CharField(validators=[airport_regex],primary_key = True,max_length=5)
	airport_name = models.CharField(max_length=20)
	airport_country = models.CharField(max_length=20)
	airport_city = models.CharField(max_length=20)
	airport_news  = models.CharField(max_length=1000)

class Flight(models.Model):
	flight_regex = RegexValidator(regex=r'^[1-9]\d{9,9}$', message="Flight id must be entered in the format: '1000000000'. A 10 digit number not starting with 0.")
	price_regex = RegexValidator(regex=r'^\d+(\.\d{1,2})?$', message="Valid Price must be entered in the format: '5000.05 or 5000'.")
	count_regex = RegexValidator(regex=r'^\d+$', message="Enter valid number of seats")
	time_regex = RegexValidator(regex=r'^((1[0-2]|0?[1-9]):([0-5][0-9]) ([AaPp][Mm]))$', message="Enter valid time of format HH:MM AM/PM 12hour")
	count1_regex = RegexValidator(regex=r'^\d$', message="Enter valid offset")
	flight_id = models.CharField(validators=[flight_regex],primary_key = True,max_length=10)
	business_classfare = models.CharField(validators=[price_regex],max_length=15)
	economy_classfare = models.CharField(validators=[price_regex],max_length=15)
	total_bseats = models.CharField(validators=[count_regex],max_length=4)
	total_eseats = models.CharField(validators=[count_regex],max_length=4)
	airline_email = models.ForeignKey(Airline,on_delete=models.CASCADE)
	daysoffset = models.CharField(validators=[count1_regex],max_length=1)
	num_intermediate_stops = models.CharField(max_length = 2,default="0")
	sourceid = models.ForeignKey(Airport,on_delete=models.CASCADE, related_name="sourceid")
	destinationid = models.ForeignKey(Airport,on_delete=models.CASCADE, related_name="destinationid")
	departure_time = models.CharField(validators=[time_regex],max_length=8)
	arrival_time = models.CharField(validators=[time_regex],max_length=8)

class IntermediateStop(models.Model):
	time_regex = RegexValidator(regex=r'^((1[0-2]|0?[1-9]):([0-5][0-9]) ([AaPp][Mm]))$', message="Enter valid time of format HH:MM 24hour")
	count1_regex = RegexValidator(regex=r'^\d$', message="Enter valid offset")
	flight_id = models.ForeignKey(Flight,on_delete=models.CASCADE)
	stop_id = models.ForeignKey(Airport,on_delete=models.CASCADE)
	daysoffset = models.CharField(validators=[count1_regex],max_length=1)
	departure_time = models.CharField(validators=[time_regex],max_length=8)
	arrival_time = models.CharField(validators=[time_regex],max_length=8)
	stop_rank = models.IntegerField(default=0)
	class IntermediateStop_Meta:
		uniquetogether= ('flight_id', 'stop_id')

class Flight_instance(models.Model):
	count_regex = RegexValidator(regex=r'^\d+$', message="Enter valid number of seats")
	date_regex = RegexValidator(regex=r'^\s*(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})\s*$', message="Enter valid date")
	flight_id = models.ForeignKey(Flight,on_delete=models.CASCADE)
	date_of_departure = models.CharField(validators=[date_regex],max_length=10)
	available_bseats = models.CharField(validators=[count_regex],max_length=4)
	available_eseats = models.CharField(validators=[count_regex],max_length=4)
	class Flight_instance_Meta:
		uniquetogether= ('flight_id', 'date_of_departure')

class Offers(models.Model):
	date_regex = RegexValidator(regex=r'^\s*(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})\s*$', message="Enter valid date")
	offer_id = models.CharField(primary_key = True,max_length=10)
	startdate = models.CharField(validators=[date_regex],max_length=10)
	end_date = models.CharField(validators=[date_regex],max_length=10)
	description = models.TextField(blank=True, null=True)
	flight_id = models.ForeignKey(Flight,on_delete=models.CASCADE,default=None)


# class ValidOffers(models.Model):
# 	passenger_email = models.ForeignKey(Passenger,on_delete=models.CASCADE)
# 	offer_id = models.ForeignKey(Offers,on_delete=models.CASCADE)
# 	class ValidOffers_Meta:
# 		uniquetogether= ('passenger_email', 'offer_id')

# class OfferedBy(models.Model):
# 	airline_email = models.ForeignKey(Airline,on_delete=models.CASCADE)
# 	offer_id = models.ForeignKey(Offers,on_delete=models.CASCADE)
# 	class OfferedBy_Meta:
# 		uniquetogether= ('airline_email', 'offer_id')

# class AvailableWeekDays(models.Model):
# 	flight_id = models.ForeignKey(Flight,on_delete=models.CASCADE)
# 	day_regex = RegexValidator(regex=r'^Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday$',message="Enter Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday")
# 	week_day = models.CharField(validators=[day_regex],max_length=10)
# 	class AvailableWeekDays_Meta:
# 		uniquetogether= ('flight_id', 'week_day')

class Ticket(models.Model):
    ticket_regex = RegexValidator(regex=r'^[1-9]\d{9,9}$', message="Ticket id must be entered in the format: '1000000000'. A 10 digit number not starting with 0.")
    date_regex = RegexValidator(regex=r'^\s*(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})\s*$', message="Enter valid date")
    fare_regex = RegexValidator(regex=r'^\d+(\.\d{1,2})?$', message="Valid fare must be entered in the format: '5000.05 or 5000'.")
    status_regex = RegexValidator(regex=r'^Booked|Waiting$')
    ticket_id = models.CharField(validators=[ticket_regex],primary_key = True,max_length=10)
    passenger_email = models.ForeignKey(Passenger,on_delete=models.CASCADE)
    flight_id = models.ForeignKey(Flight,on_delete=models.CASCADE)
    date_of_departure = models.CharField(validators=[date_regex],max_length=10)
    flight_class = models.CharField(max_length=10,default='')
    rating = models.CharField(max_length=1,default='')
    status = models.CharField(validators=[status_regex],max_length=10,default='')


class RelevantAirports(models.Model):
	email = models.ForeignKey(Passenger,on_delete=models.CASCADE)
	airport_id = models.ForeignKey(Airport,on_delete=models.CASCADE)
	class RelevantAirports_meta:
		uniquetogether = ('email','airport_id')
