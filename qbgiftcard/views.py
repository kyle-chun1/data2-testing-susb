from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def qbgiftcardhome(request):
    return render(request, 'qbgiftcard/lookup.html', {})

def results(request):
    return HttpResponse('working - results')

def lookup(request):
    return HttpResponse('working - lookup')

def giftcard(request):
    return HttpResponse('working - giftcard')

def log(request):
    return HttpResponse('working - log')
