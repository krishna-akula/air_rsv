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

@ensure_csrf_cookie
def change_password(request):
    if request.method == "POST":
        if request.session['type'] == 'passenger':
            passenger = Passenger.objects.get(email = request.session['id'])
            oldpassword = request.POST.get('oldpassword')
            newpassword = request.POST.get('newpassword')
            if passenger.check_password(oldpassword):
                passenger.set_password(passenger.make_password(newpassword))
                passenger.save()
            else:
                messages.error(request,'Old Password Incorrect')
            return redirect('/')
        elif request.session['type'] == 'airline':
            airline = Airline.objects.get(email = request.session['id'])
            oldpassword = request.POST.get('oldpassword')
            newpassword = request.POST.get('newpassword')
            if airline.check_password(oldpassword):
                airline.set_password(airline.make_password(newpassword))
                airline.save()
            else:
                messages.error(request,'Old Password Incorrect')
            return redirect('/')
    else:
        if request.session['type'] == 'passenger':
            return render(request,"air_rsv/change_password_user.html")
        else :
            return render(request,"air_rsv/change_password_airline.html")

def home(request):
    if 'id' in request.session.keys():
        if request.session['type'] == 'passenger':
            print request.session['id']
            passenger = Passenger.objects.get(email = request.session['id'])
            context = {'object' : passenger,'base':'base_user.html'}
            return render(request,'air_rsv/user_profile.html', context)
        elif request.session['type'] == 'airline':
            airline = Airline.objects.get(email=request.session['id'])
            context = {'object': airline, 'base': 'base_airline.html'}
            return render(request,'air_rsv/user_profile.html',context)
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
            request.session['id'] = email
        elif  usertype == 'airline':
            user = Airline(email = email,firstname=firstname,lastname=lastname, password = password, phonenumber = phonenumber)
            user.set_password(user.make_password(password))
            user.save()
            request.session['type'] = 'airline'
            request.session['id'] = email
        return redirect('/')
    if request.method == 'GET':
        return render(request,'air_rsv/register.html')


@ensure_csrf_cookie
def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            passenger = Passenger.objects.get(email=email)
            if passenger.check_password(password):
                request.session['id'] = email
                request.session['type'] = 'passenger'
                return redirect('/')
            else:
                messages.error(request,'Password Incorrect')
                return redirect('/signin')
        except:
            try:
                airline = get_object_or_404(Airline, email=email)
                if airline.check_password(password):
                    request.session['id'] = email
                    request.session['type'] = 'airline'
                    return redirect('/')
                else:
                    messages.error(request,'Password Incorrect')
                    return redirect('/signin')
            except:
                messages.error(request,'No Passenger or Airline is registered with this email')
                return redirect('/signin')

    elif request.method == 'GET':
        return render(request,'air_rsv/signin.html')

def logout(request):
    try:
        del request.session['id']
        del request.session['type']
        request.session.modified = True
    except KeyError:
        pass
    return render(request, 'air_rsv/home.html')

