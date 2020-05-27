from django.contrib import admin
from django.urls import path



from shopify.views import acetap,lookup,queued


urlpatterns = [
    path('acetap/', acetap, name='acetap'),
    path('lookup/', lookup, name='lookup'),
    path('queued/', queued, name='queued'),
]
