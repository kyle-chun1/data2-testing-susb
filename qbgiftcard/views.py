from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from qbgiftcard.models import GiftCard

from json import dumps

def qbgiftcardhome(request):
    G = GiftCard.objects.all()
    customer_dict = []
    for i in G:
        customer_dict.append([i.id, i.first_name, i.last_name, i.phone, i.email ])
    return render(request, 'qbgiftcard/lookup.html', {'customer_dict': dumps(customer_dict)})




def results(request):
    G = GiftCard.objects.all()
    customer_dict = []
    for i in G:
        customer_dict.append([i.id, i.first_name, i.last_name, i.phone, i.email ])    
    return render(request, 'qbgiftcard/lookup_temp.html', {'customer_dict': dumps(customer_dict)})

def lookup(request):
    return HttpResponse('working - lookup')

def giftcard(request):
    return HttpResponse('working - giftcard')

def log(request):
    return HttpResponse('working - log')
