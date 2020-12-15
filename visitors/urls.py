from django.contrib import admin
from django.urls import path


from visitors.views import *

urlpatterns = [

    path('submit/', submit, name='submit'),
    path('capacity/', capacity, name='capacity'),
    path('hourly/<slug:location>/', visitors_hourly, name='visitors_hourly'),

    # PUT ALL VIEW ABOVE THIS OR ELSR THE BELOW VIEW HITS AND RETURNS HOME!
    path('<slug:location>/', VISITORS, name='VISITORS'),


]
