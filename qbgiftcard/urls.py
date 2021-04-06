from django.urls import path

from qbgiftcard.views import *

app_name='qbgiftcard'

urlpatterns = [
    path('', qbgiftcardhome, name='qbgiftcardhome'),

    path('results/', results, name='results'),

    path('lookup/', lookup, name='lookup'),

    path('giftcard/', giftcard, name='giftcard'),

    path('log/', log, name='log'),

]
