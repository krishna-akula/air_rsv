from django.conf.urls import url,include
from django.contrib import admin
import views

app_name="air_rsv"
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^register/$', views.signup, name="register"),
    url(r'^signin/$', views.signin, name="signin"),
    url(r'^home/?$',views.home, name='home'),
    url(r'^logout/?$',views.logout, name='logout'),
    # url(r'^bookticket/?$',views.bookticket, name='bookticket'),
    url(r'^change_password/?$', views.change_password, name='change_password'),
    url(r'^add_flight/?$', views.add_flight, name='add_flight'),
    url(r'^remove_flight/?$', views.remove_flight, name='remove_flight'),
    url(r'^flight_data/?$', views.flight_data, name='flight_data'),
    url(r'^flight_search/?$', views.flight_search, name='flight_search'),
    url(r'^offeradd/?$', views.offeradd, name='offeradd'),
    url(r'^offerremove/?$', views.offerremove, name='offerremove'),
    url(r'^offersdata/?$', views.offersdata, name='offersdata'),
    url(r'^airportsdata/?$', views.airportsdata, name='airportsdata'),
    url(r'^show_flights/?$', views.show_flights, name='show_flights'),
    # url(r'^book_conform/?$', views.book_conform, name='book_conform'),

]
