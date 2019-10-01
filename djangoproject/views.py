from django.http import HttpResponse
from django.shortcuts import render
from django.utils.timezone import datetime

def mm(request):


    return_dict = {'tDate':str(datetime.today())[0:10]}

    return  render(request, 'material.html',return_dict)

    # return HttpResponse()
