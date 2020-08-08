from django.contrib import admin
from django.urls import path


from visitors.views import *

urlpatterns = [

    path('submit/', submit, name='submit'),
    path('<slug:location>/', VISITORS, name='VISITORS'),

]
