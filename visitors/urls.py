from django.contrib import admin
from django.urls import path


from visitors.views import *

urlpatterns = [
    path('irc/', irc, name='irc'),
    path('trc/', trc, name='trc'),
    path('ddo/', ddo, name='ddo'),
    path('rch/', rch, name='rch'),
    path('test/', test, name='test'),
    path('submit/', submit, name='submit')
]
