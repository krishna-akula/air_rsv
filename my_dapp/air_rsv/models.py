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
	type = models.IntegerField(default=0)
	# phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.") #############look into regex
	# phone = models.CharField(validators=[phone_regex],max_length=15,blank = True)
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

class Airline(models.Model):
    # username = models.CharField(primary_key=True,max_length =50)
	email = models.EmailField(primary_key = True)
	password = models.CharField(max_length=100)
	firstname = models.CharField(max_length=200)
	lastname = models.CharField(max_length=200)
	type = models.IntegerField(default=0)
	# phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.") #############look into regex
	# phone = models.CharField(validators=[phone_regex],max_length=15,blank = True)
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


