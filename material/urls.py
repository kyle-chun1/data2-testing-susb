from django.urls import path

from material.views import *

app_name='material'

urlpatterns = [
    path('', materialhome, name='materialhome'),

]
