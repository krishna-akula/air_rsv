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
    url(r'^change_password/?$', views.logout, name='change_password'),
]
