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
from datetime import datetime, timedelta, date
from django.db import transaction
import hashlib

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

def update_tid(ticket_id):
    global tid
    tid = ticket_id
    

@ensure_csrf_cookie
def change_password(request):
    if request.method == "POST":
        if request.session['type'] == 'passenger':
            passenger = Passenger.objects.get(email = request.session['id'])
            oldpassword = request.POST.get('oldpassword')
            newpassword = request.POST.get('newpassword')
            newpassword1 = request.POST.get('newpassword1')
            if passenger.check_password(oldpassword) and newpassword == newpassword1:
                passenger.set_password(passenger.make_password(newpassword))
                passenger.save()
                return redirect('/')
            elif passenger.check_password(oldpassword) == False:
                messages.error(request,'Old Password Incorrect')
            else:
                messages.error(request, 'Confirmation password mismatch')
            return redirect('/change_password')
        elif request.session['type'] == 'airline':
            airline = Airline.objects.get(email = request.session['id'])
            oldpassword = request.POST.get('oldpassword')
            newpassword = request.POST.get('newpassword')
            newpassword1 = request.POST.get('newpassword1')
            if airline.check_password(oldpassword) and newpassword == newpassword1:
                airline.set_password(airline.make_password(newpassword))
                airline.save()
                return redirect('/')
            elif airline.check_password(oldpassword) == False:
                messages.error(request,'Old Password Incorrect')
            else:
                messages.error(request, 'Confirmation password mismatch')
            return redirect('/change_password')
    else:
        if request.session['type'] == 'passenger':
            return render(request,"air_rsv/change_password_user.html",{'base':'base_user.html'})
        else :
            return render(request,"air_rsv/change_password_user.html",{'base':'base_airline.html'})

def home(request):
    if 'id' in request.session.keys():
        data = Airport.objects.all() # change this to relevant airports
        if request.session['type'] == 'passenger':
            passenger = Passenger.objects.get(email = request.session['id'])
            context = {'object' : passenger,'base':'base_user.html','data' : data}
            return render(request,'air_rsv/user_profile.html', context)
        elif request.session['type'] == 'airline':
            airline = Airline.objects.get(email=request.session['id'])
            context = {'object': airline, 'base': 'base_airline.html','data' : data}
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
        phonenumber = request.POST.get('phonenumber')
        if usertype == 'passenger':
            try:
                Passenger.objects.get(email=email)
                messages.error(request, "Email already exists")
                return redirect('/register')                
            except:
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
                return redirect('/')

        elif  usertype == 'airline':
            try:
                Airline.objects.get(email=email)
                messages.error(request, "Email already exists")
                return redirect('/register')                
            except:
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
        usertype = request.POST.get('usertype')
        if usertype == 'passenger':
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
                messages.error(request,'No User is registered with this email')
                return redirect('/signin')
        elif usertype == 'airline':
            try:
                airline = Airline.objects.get(email=email)
                if airline.check_password(password):
                    request.session['id'] = email
                    request.session['type'] = 'airline'
                    return redirect('/')
                else:
                    messages.error(request,'Password Incorrect')
                    return redirect('/signin')
            except:
                messages.error(request,'No Airline is registered with this email')
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
        if (Flight.objects.get(flight_id = flightid)).count() != 0:
            messages.error(request, 'Flight ID already exists')
            return redirect('/add_flight')
        business_fare = request.POST['business_fare']
        economy_fare = request.POST['economy_fare']
        total_bseats = request.POST['total_bseats']
        total_eseats = request.POST['total_eseats']
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

def get_tot(td):
    hr = int(td)
    mn = int((td - hr) * 60)
    return str(hr) + " : " + str(mn)

all_results = dict()
@ensure_csrf_cookie
def flight_search(request):
    if 'id' in request.session.keys() and request.session['type'] == 'passenger':
        if request.method == 'POST':
            ffrom = request.POST.get('from')
            fto = request.POST.get('to')
            fdate = request.POST.get('date')
            ftotal_seats = int(request.POST.get('total_seats'))
            fclass = request.POST.get('class')
            results_list = []
            results_from = Airport.objects.filter(Q(airport_name__contains=ffrom) | Q(airport_city__contains=ffrom))
            results_to = Airport.objects.filter(Q(airport_name__contains=fto) | Q(airport_city__contains=fto))
            try:
                fdate_ob = datetime.strptime(fdate, '%Y-%m-%d').date()
                if fdate_ob < date.today() :
                    raise Exception('date error!')
            except:
                messages.error(request,'Enter a valid Date')
                return redirect('/flight_search')
            for sid in results_from:
                for did in results_to:
                    for flg in Flight.objects.all():
                        if flg.sourceid.airport_id == sid.airport_id and flg.destinationid.airport_id  == did.airport_id:
                            t1 = datetime.combine(fdate_ob, datetime.strptime(flg.departure_time, '%H:%M').time())
                            t2 = datetime.combine(fdate_ob + timedelta(days=int(flg.daysoffset)), datetime.strptime(flg.arrival_time, '%H:%M').time())
                            results_list.append((flg, None, int((t2 - t1).days) * 24 + (t2- t1).seconds/3600.0,flg.sourceid ,flg.destinationid))
                        for inter in IntermediateStop.objects.filter(flight_id = flg.flight_id):
                            if flg.sourceid.airport_id == sid.airport_id and inter.stop_id.airport_id == did.airport_id:
                                t1 = datetime.combine(fdate_ob, datetime.strptime(flg.departure_time, '%H:%M').time())
                            	t2 = datetime.combine(fdate_ob + timedelta(days=int(inter.daysoffset)), datetime.strptime(inter.arrival_time, '%H:%M').time())
                                results_list.append((flg, None, int((t2 - t1).days) * 24 + (t2- t1).seconds/3600.0,flg.sourceid,inter.stop_id))  
                            if inter.stop_id.airport_id == sid.airport_id and flg.destinationid.airport_id  == did.airport_id:
                                t1 = datetime.combine(fdate_ob, datetime.strptime(inter.departure_time, '%H:%M').time())
                            	t2 = datetime.combine(fdate_ob + timedelta(days=int(flg.daysoffset) - int(inter.daysoffset)), datetime.strptime(flg.arrival_time, '%H:%M').time())
                                results_list.append((flg, inter, int((t2 - t1).days) * 24 + (t2- t1).seconds/3600.0,inter.stop_id,flg.destinationid))  
                        for inter1 in IntermediateStop.objects.filter(flight_id = flg.flight_id):
                            for inter2 in IntermediateStop.objects.filter(flight_id = flg.flight_id):
                                if inter1.stop_rank < inter2.stop_rank:
                                    if inter1.stop_id.airport_id == sid.airport_id and inter2.stop_id.airport_id == did.airport_id:
                                        t1 = datetime.combine(fdate_ob, datetime.strptime(inter1.departure_time, '%H:%M').time())
                                        t2 = datetime.combine(fdate_ob + timedelta(days=int(inter2.daysoffset) - int(inter1.daysoffset)), datetime.strptime(inter2.arrival_time, '%H:%M').time())
                                        results_list.append((flg, inter1, int((t2 - t1).days) * 24 + (t2- t1).seconds/3600.0,inter1.stop_id,inter2.stop_id))
            

            final_results = []
            for res, inter_ob, tot, sid, did in results_list:
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
                if (int(tmp) >= int(ftotal_seats)) :
                    try:
                        go = Offers.objects.get(flight_id = flgi0.flight_id)
                        if (not(date.today() <= go.end_date and go.startdate <= date.today())):
                            raise Exception('Yo')
                    except:
                        go = None
                    
                    final_results.append([res, inter_ob, fclass,fare, fdate, ftotal_seats,go,get_tot(tot),sid,did]) # start and end time            
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
        discount = request.POST['discount']
        offer = Offers(offer_id = offerid,	startdate = startdate,	end_date = enddate,	discount = discount,
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

f_results = dict()
@ensure_csrf_cookie
def show_flights(request):
    final_results=all_results[request.session['id']]
    if request.method=="POST":
        i = 1
        final_results=all_results[request.session['id']]
        for fres in final_results:
            if request.POST.get('rb','0')==str(i):
                f_results[request.session['id']]=final_results[i-1]
                # return render(request,'air_rsv/booking_conform.html',{"ticket_data":final_results[i-1]})
                return redirect('/booking_conform')
            else:
                i = i + 1
    else:
        return render(request,'air_rsv/show_flights.html',{'final_results':final_results})

@ensure_csrf_cookie
@transaction.atomic
def booking_conform(request):
    if request.method=="POST":
        result = f_results[request.session['id']]
        i = result[0]
        j = result[1]
        k = result[2]
        l = result[3]
        m = result[4]
        n = result[5]
        p = result[6]
        # sourid = result[8]
        # destid = result[9]
        s=i.flight_id+str(m)
        # generate unique ticketid
        #update_tid(ticket_id)
        passenger_email = Passenger.objects.get(email=request.session['id'])
        # source_port = Airport.objects.get(airport_id = sourid)
        # dest_port = Airport.objects.get(airport_id = destid)
        flight_id = i
        date_of_departure = m
        ftotal_seats = n
        flight_class = k
        flgi = Flight_instance.objects.get(flight_id = i, date_of_departure = m)
        available_bseats = int(flgi.available_bseats)
        available_eseats = int(flgi.available_eseats)
        s += flgi.available_bseats+flgi.available_eseats
        s = int(int(hashlib.sha1(s).hexdigest(), 16) % (10 ** 10))
        ticketinstance = Ticket(ticket_id = str(s),passenger_email = passenger_email,flight_id = flight_id,date_of_departure = date_of_departure,flight_class = flight_class,total_seats = ftotal_seats,source_id = result[8],destination_id=result[9])
        ticketinstance.save()
        if(k == "business"):
            available_bseats = int(flgi.available_bseats) - (int(l)/int(i.business_classfare))
        else :
            available_eseats = int(flgi.available_eseats) - (int(l)/int(i.economy_classfare))
        nflgi = Flight_instance(flight_id = i, date_of_departure = m, available_bseats = str(available_bseats), available_eseats = str(available_eseats))
        flgi.delete()
        nflgi.save()
        f_results.clear()
        all_results.clear()
        return redirect('/booked_tickets')
    else:
        data = f_results[request.session['id']]
        # update data[3] if offers available
        if data[6] :
            data[3] = int(data[3]) - (int(data[3])*int(data[6].discount)/100) 
        return render(request,'air_rsv/booking_conform.html',{"ticket_data": data})
        
def booked_tickets(request):
    if 'id' in request.session.keys():
        tickets = Ticket.objects.filter(passenger_email = request.session['id'])
        data = []
        for t in tickets:
            data.append(t)
        return render(request,'air_rsv/booked_tickets.html',{"data":data})
    else:
        return redirect('/')

@transaction.atomic
def cancel_ticket(request):
    if request.method=="POST":
        ticketinstance=Ticket.objects.get(ticket_id=request.POST['ticket_id'])
        flight_id = ticketinstance.flight_id.flight_id
        fclass = ticketinstance.flight_class
        ftotalseats = ticketinstance.total_seats
        dod = ticketinstance.date_of_departure
        flightinstance = Flight_instance.objects.get(flight_id = flight_id,date_of_departure = dod)
        available_bseats = int(flightinstance.available_bseats)
        available_eseats = int(flightinstance.available_eseats)
        if(fclass == "business"):
             available_bseats = int(flightinstance.available_bseats) + int(ftotalseats)
        else:
            available_eseats = int(flightinstance.available_eseats) + int(ftotalseats)
        nflgi = Flight_instance(flight_id = flightinstance.flight_id, date_of_departure = dod, available_bseats = str(available_bseats), available_eseats = str(available_eseats))
        flightinstance.delete()
        nflgi.save()
        ticketinstance.delete()
        return redirect('/')
    else:
        return render(request,'air_rsv/cancel_ticket.html')
