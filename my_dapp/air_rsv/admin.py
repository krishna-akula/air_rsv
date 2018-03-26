# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Passenger)
admin.site.register(Airline)
admin.site.register(Airport)
admin.site.register(Flight)
admin.site.register(Flight_instance)
admin.site.register(IntermediateStop)
admin.site.register(Offers)
# admin.site.register(ValidOffers)
# admin.site.register(OfferedBy)
admin.site.register(Ticket)
# admin.site.register(AvailableWeekDays)
# admin.site.register(RelevantAirports)