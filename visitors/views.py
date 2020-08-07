from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseNotFound, JsonResponse

# Create your views here.

from visitors.models import Visitors
from django.db.models import Sum


def irc(request):
    #IF USER IS NOT AUTHENTICATED SEND THEM HOME!
    if not request.user.is_authenticated:
        return redirect('HOME')
    current = Visitors.objects.filter(location='IRC').aggregate(Sum('count'))['count__sum']
    return render(request, 'visitors/index.html',{'location':'IRC', 'current':current})

def trc(request):
    #IF USER IS NOT AUTHENTICATED SEND THEM HOME!
    if not request.user.is_authenticated:
        return redirect('HOME')
    current = Visitors.objects.filter(location='TRC').aggregate(Sum('count'))['count__sum']
    return render(request, 'visitors/index.html',{'location':'TRC', 'current':current})

def rch(request):
    #IF USER IS NOT AUTHENTICATED SEND THEM HOME!
    if not request.user.is_authenticated:
        return redirect('HOME')
    current = Visitors.objects.filter(location='RCH').aggregate(Sum('count'))['count__sum']
    return render(request, 'visitors/index.html',{'location':'RCH', 'current':current})

def ddo(request):
    #IF USER IS NOT AUTHENTICATED SEND THEM HOME!
    if not request.user.is_authenticated:
        return redirect('HOME')
    current = Visitors.objects.filter(location='DDO').aggregate(Sum('count'))['count__sum']
    return render(request, 'visitors/index.html',{'location':'DDO', 'current':current})

def test(request):
    #IF USER IS NOT AUTHENTICATED SEND THEM HOME!
    if not request.user.is_authenticated:
        return redirect('HOME')
    current = Visitors.objects.filter(location='TEST').aggregate(Sum('count'))['count__sum']
    return render(request, 'visitors/index.html',{'location':'TEST', 'current':current})





from visitors.models import Visitors
from django.utils import timezone

def submit(request):  #ASUME LOCATIONS ARE CORRECT
    #IF USER IS NOT AUTHENTICATED SEND THEM HOME!
    if not request.user.is_authenticated:
        return redirect('HOME')

# HARCOCDED LOCATIONS!!!!!!!!!!!!!!!!
    if 'location' in request.POST and str(request.POST['location']) not in ['IRC','TRC','DDO','RCH','TEST']:
        location = 'TEST'
    else:
        location = request.POST['location']

    try:
        flr_email = request.user.email
        count = int(request.POST['count'])
        if count > 5:
            count = 5
        if count <-5:
            count = -5
    except:
        return redirect('/visitors/test')

    ##############################
    if count != 0 :
        Visitors(timestamp=timezone.now(),flr_email=flr_email,count=count,location=location).save()

    return redirect('/visitors/' + location.lower() + '/')
