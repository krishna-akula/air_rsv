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
from django.core.exceptions import ValidationError
from models import *
from django.db.models import Q
from datetime import datetime, timedelta

def phone_valid(value):
    val = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
                                 code='invalid_phonenumber')
    try :
        val=val(value)
        return None
    except:
        return "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."


def date_valid(value):
    val = RegexValidator(regex=r'^\s*(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})\s*$',
                                message="Enter valid date")
    try:
        val(value)
        return None
    except:
        return "Enter valid date"

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
            return render(request,"air_rsv/change_password_user.html",{'base':'base_user.html'})
        else :
            return render(request,"air_rsv/change_password_user.html",{'base':'base_airline.html'})

def home(request):
    if 'id' in request.session.keys():
        if request.session['type'] == 'passenger':
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
    if 'id' in request.session.keys():
        if request.session['type'] == 'passenger':
            passenger = Passenger.objects.get(email = request.session['id'])
            context = {'object' : passenger,'base':'base_user.html'}
            return render(request,'air_rsv/user_profile.html', context)
        elif request.session['type'] == 'airline':
            airline = Airline.objects.get(email=request.session['id'])
            context = {'object': airline, 'base': 'base_airline.html'}
            return render(request,'air_rsv/user_profile.html',context)

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
            # checking the regex
            error = phone_valid(user.phonenumber)
            if error is None:
                user.save()
            else:
                messages.error(request, error)
                return redirect('/register')
            request.session['type'] = 'passenger'
            request.session['id'] = email
        elif  usertype == 'airline':
            user = Airline(email = email,firstname=firstname,lastname=lastname, password = password, phonenumber = phonenumber)
            user.set_password(user.make_password(password))
            # checking the regexs
            error = phone_valid(user.phonenumber)
            if error is None:
                user.save()
            else:
                messages.error(request, error)
                return redirect('/register')
            request.session['type'] = 'airline'
            request.session['id'] = email
        return redirect('/')
    if request.method == 'GET':
        return render(request,'air_rsv/register.html')


@ensure_csrf_cookie
def signin(request):

    if 'id' in request.session.keys():
        if request.session['type'] == 'passenger':
            passenger = Passenger.objects.get(email=request.session['id'])
            context = {'object': passenger, 'base': 'base_user.html'}
            return render(request, 'air_rsv/user_profile.html', context)
        elif request.session['type'] == 'airline':
            airline = Airline.objects.get(email=request.session['id'])
            context = {'object': airline, 'base': 'base_airline.html'}
            return render(request, 'air_rsv/user_profile.html', context)

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


@ensure_csrf_cookie
def add_flight(request):
    if request.method=="POST":
        flightid = request.POST['flightid']
        business_fare = request.POST['business_fare']
        economy_fare = request.POST['economy_fare']
        total_bseats = request.POST['total_bseats']
        total_eseats = request.POST['total_eseats']
        airline_email = Airline.objects.get(email= request.POST['airline_id'])
        source_id = Airport.objects.get(airport_id=request.POST['source_id'])
        source_dep = request.POST['source_dep']
        destination_id = Airport.objects.get(airport_id=request.POST['destination_id'])
        destination_arr = request.POST['destination_arr']
        day_offset = request.POST['day_offset']
        intermediate_stops = request.POST['intermediate_stops']
        flight=Flight(flight_id = flightid,	business_classfare = business_fare,num_intermediate_stops = intermediate_stops,economy_classfare = economy_fare,	total_bseats =total_bseats ,total_eseats =total_eseats,
	            airline_email = airline_email,	daysoffset = day_offset,sourceid = source_id,	destinationid = destination_id ,	departure_time = source_dep,arrival_time = destination_arr)
        flight.save()
        key_ar="inter_arrtime"
        key_dest_id="destination_id"
        key_inter_dp="inter_deptime"
        key_id_off="interday_offset"
        print intermediate_stops,"asdfghj"
        for i in range(1,int(intermediate_stops)+1):
            inter_arrtime=request.POST[key_ar+str(i)]
            destination_id=Airport.objects.get(airport_id=request.POST[key_dest_id+str(i)])
            inter_deptime=request.POST[key_inter_dp+str(i)]
            interday_offset=request.POST[key_id_off+str(i)]
            int_med_stop=IntermediateStop(flight_id = flight,stop_id =destination_id ,daysoffset = interday_offset,	departure_time = inter_deptime,
                                          arrival_time = inter_arrtime,stop_rank=i)
            int_med_stop.save()
        return redirect('/')
    else:
        return render(request,'air_rsv/flightadd.html')

def remove_flight(request):
    if request.method=="POST":
        flight=Flight.objects.get(flight_id=request.POST['flight_id'])
        flight.delete()
        return redirect('/')
    else:
        return render(request,'air_rsv/flightremove.html')

def flight_data(request):
    airline=Airline.objects.get(email=request.session['id'])
    flight_obj=Flight.objects.filter(airline_email=airline)
    return render(request,'air_rsv/flight_data.html',{'flight':flight_obj})

all_results = dict()
@ensure_csrf_cookie
def flight_search(request):
    if 'id' in request.session.keys() and request.session['type'] == 'passenger':
        if request.method == 'POST':
            ffrom = request.POST.get('from')
            fto = request.POST.get('to')
            fdate = request.POST.get('date')
            ftotal_seats = request.POST.get('total_seats')
            fclass = request.POST.get('class')
            results_list = []
            results_from = Airport.objects.filter(Q(airport_name__contains=ffrom) | Q(airport_city__contains=ffrom))
            results_to = Airport.objects.filter(Q(airport_name__contains=fto) | Q(airport_city__contains=fto))
            for sid in results_from:
                for did in results_to:
                    for flg in Flight.objects.all():
                        if flg.sourceid.airport_id == sid.airport_id and flg.destinationid.airport_id  == did.airport_id:
                            results_list.append((flg, None))
                        for inter in IntermediateStop.objects.filter(flight_id = flg.flight_id):
                            if flg.sourceid.airport_id == sid.airport_id and inter.stop_id.airport_id == did.airport_id:
                                results_list.append((flg, None))  
                            if inter.stop_id.airport_id == sid.airport_id and flg.destinationid.airport_id  == did.airport_id:
                                results_list.append((flg, inter))
                        for inter1 in IntermediateStop.objects.filter(flight_id = flg.flight_id):
                            for inter2 in IntermediateStop.objects.filter(flight_id = flg.flight_id):
                                if inter1.stop_rank < inter2.stop_rank:
                                    if inter1.stop_id.airport_id == sid.airport_id and inter2.stop_id.airport_id == did.airport_id:
                                        results_list.append((flg, inter1))
            fdate_ob = datetime.strptime(fdate, '%Y-%m-%d').date()
            final_results = []
            for res, inter_ob in results_list:
                if (inter_ob == None):
                    dod = fdate_ob
                else:
                    dod = fdate_ob - timedelta(days = (int)(inter_ob.daysoffset))
                
                flgi = Flight_instance.objects.filter(flight_id = res.flight_id, date_of_departure = dod)
                if flgi.count() == 0: 
                    nflgi = Flight_instance(flight_id = Flight.objects.get(flight_id=res.flight_id), date_of_departure = dod, available_bseats = res.total_bseats, available_eseats = res.total_eseats)
                    nflgi.save()
                    flgi0 = nflgi
                else :
                    flgi0 = flgi[0]

                if (fclass == "business"):
                    tmp = flgi0.available_bseats
                    fare = int(ftotal_seats)*int(res.business_classfare)
                else :
                    tmp = flgi0.available_eseats
                    fare = int(ftotal_seats)*int(res.economy_classfare)
                print fare
                if (tmp >= ftotal_seats) :
                    final_results.append((res, inter_ob, fare, fdate, Offers.objects.filter(flight_id = flgi0.flight_id))) # start and end time
            
            all_results[request.session['id']]=final_results
            return redirect('/show_flights')
        if request.method == 'GET': 
            return render(request,'air_rsv/flight_search.html')
    else :
        return redirect('/')

def offeradd(request):
    if request.method=="POST":
        flightid = Flight.objects.get(flight_id=request.POST['flightid'])
        offerid = request.POST['offerid']
        startdate = request.POST['startdate']
        enddate = request.POST['enddate']
        description = request.POST['description']
        offer = Offers(offer_id = offerid,	startdate = startdate,	end_date = enddate,	description = description,
	                        flight_id = flightid)
        offer.save()
        return redirect('/')
    else:
        return render(request,'air_rsv/offeradd.html')

def offerremove(request):
    if request.method=="POST":
        offer=Offers.objects.get(offer_id = request.POST['offerid']) 
        offer.delete()
        return redirect('/')
    else:
        return render(request,'air_rsv/offerremove.html')

def offersdata(request):
    if 'id' in request.session.keys():
        flight=Flight.objects.filter(airline_email=request.session['id'])
        data=[]
        for i in flight:
            data.append(Offers.objects.filter(flight_id=i.flight_id))
        return render(request,'air_rsv/offersdata.html',{"data":data})
    else:
        return redirect('/')

def airportsdata(request):
    if 'id' in request.session.keys():
        data = Airport.objects.all()
        return render(request,'air_rsv/airportsdata.html',{"data":data})        
    else:
        return redirect('/')

@ensure_csrf_cookie
def show_flights(request):
	if request.method=="POST":
		i = 1
		final_results=all_results[request.session['id']]
		for fres in final_results:
			if request.POST[('rb'+str(i))]==str(i):
				return render(request,'air_rsv/booking_conform.html')
			else:
				i = i + 1
	else:
		print all_results
		return render(request,'air_rsv/show_flights.html',{'final_results':all_results[request.session['id']]})

# @ensure_csrf_cookie
# def book_conform(request):
# 	if request.method=="POST":
# 		pass
# 	else:
# 		return render

