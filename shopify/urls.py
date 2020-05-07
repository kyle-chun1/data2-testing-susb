from django.contrib import admin
from django.urls import path



from shopify.views import acetap


urlpatterns = [

    path('acetap/', acetap, name='acetap'),
]
