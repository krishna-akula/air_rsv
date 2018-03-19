# -*- coding: utf-8 -*-
from __future__ import unicode_literals


# Create your views here.
	# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404,render, redirect
from django.http import HttpResponse
from models import *
import json
from django.views.decorators import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import messages
from django.core.exceptions import *
import datetime
from models import *

def home(request):
	if 'id' in request.session.keys():
		if request.session['type'] == 'passenger':
			return render(request,'air_rsv/user_profile.html')
		elif request.session['type'] == 'airline':
			return render(request,'air_rsv/user_profile.html') # TODO
	else:
		return render(request,"air_rsv/home.html")

@ensure_csrf_cookie
def signup(request):
	if request.method == 'POST':
		email = request.POST['email']
		firstname = request.POST['firstname']
		lastname = request.POST['lastname']
		password = request.POST.get('password')
		usertype = request.POST.get('usertype')
		print usertype
		phonenumber = request.POST.get('phonenumber')
		if usertype == 'passenger':
			user = Passenger(email = email,firstname=firstname,lastname=lastname, password = password, phonenumber = phonenumber)
			user.set_password(user.make_password(password))
			user.save()
			request.session['type'] = 'passenger'
		else: # usertype == 'airline':
			user = Airline(email = email,firstname=firstname,lastname=lastname, password = password, phonenumber = phonenumber)
			user.set_password(user.make_password(password))
			user.save()
			request.session['type'] = 'airline'
		return redirect('/')
		# return redirect('/admin/')
	if request.method == 'GET':
		return render(request,'air_rsv/register.html')


@ensure_csrf_cookie
def signin(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')
		print email
		print password
		try:
			passenger = Passenger.objects.get(email=email)
			if passenger.check_password(password):
				request.session['id'] = email
				request.session['type'] = 'passenger'
				return redirect('/')
			else:
				messages.error(request,'Password Incorrect')
				# return redirect('/')
		except:
			try:
				airline = get_object_or_404(Airline, email=email)
				if airline.check_password(password):
					request.session['id'] = email
					request.session['type'] = 'airline'
					return redirect('/')
				else:
					messages.error(request,'Password Incorrect')
					# return redirect('/')
			except:
				messages.error(request,'No Passenger or Airline is registered with this email')
				# return redirect('/')

	elif request.method == 'GET':
		return render(request,'air_rsv/signin.html')
