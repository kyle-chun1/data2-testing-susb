from django.contrib import admin
from django.urls import path


from . import views  ##importing the MM app view

urlpatterns = [
    path('', views.mm, name='mm'), ## can be deleted later
    path('submit/', views.mmsubmit,name='mmsubmit'),
    path('rawdata/', views.rawdata, name='rawdata'),
]
