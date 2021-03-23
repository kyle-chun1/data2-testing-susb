from django.urls import path

from pricing.views import pricing_portal, pricing_submit
from pricing.views import tester2, tester3, tester_main, tester_submit

app_name='pricing'

urlpatterns = [
    path('portal/<slug:location>/', pricing_portal, name='portal'),
    path('portal/<slug:location>/submit/', pricing_submit, name='submit'),

    path('tester2/', tester2, name='tester2'),
    path('tester3/', tester3, name='tester3'),
    path('tester_main/', tester_main, name='tester_main'),
    path('tester_submit/', tester_submit, name='tester_submit'),
]
