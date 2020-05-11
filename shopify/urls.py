from django.contrib import admin
from django.urls import path



from shopify.views import acetap,test


urlpatterns = [
    path('acetap/', acetap, name='acetap'),
    path('test/', test, name='test'),
]
