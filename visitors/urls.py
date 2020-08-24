from django.contrib import admin
from django.urls import path


from visitors.views import *

urlpatterns = [

    path('submit/', submit, name='submit'),
    path('capacity/', capacity, name='capacity'),
    path('hourly/', visitors_hourly, name='visitors_hourly'),
    path('<slug:location>/', VISITORS, name='VISITORS'),

]
