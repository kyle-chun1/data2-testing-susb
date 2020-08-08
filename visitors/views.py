from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseNotFound, JsonResponse

# Create your views here.

from visitors.models import Visitors
from django.db.models import Sum


def irc(request):
    #IF USER IS NOT AUTHENTICATED SEND THEM HOME!
    if not request.user.is_authenticated:
        return redirect('HOME')
    capacity = 70
    current = Visitors.objects.filter(location='IRC').aggregate(Sum('count'))['count__sum']
    total_today = Visitors.objects.filter(location='IRC').filter(timestamp__date=timezone.now()).filter(count__gte=0).aggregate(Sum('count'))['count__sum']
    return render(request, 'visitors/index.html',{'location':'IRC', 'current':current, 'capacity':capacity, 'total_today':total_today})

def trc(request):
    #IF USER IS NOT AUTHENTICATED SEND THEM HOME!
    if not request.user.is_authenticated:
        return redirect('HOME')
    capacity = 92
    current = Visitors.objects.filter(location='TRC').aggregate(Sum('count'))['count__sum']
    total_today = Visitors.objects.filter(location='TRC').filter(timestamp__date=timezone.now()).filter(count__gte=0).aggregate(Sum('count'))['count__sum']
    return render(request, 'visitors/index.html',{'location':'TRC', 'current':current, 'capacity':capacity, 'total_today':total_today})

def rch(request):
    #IF USER IS NOT AUTHENTICATED SEND THEM HOME!
    if not request.user.is_authenticated:
        return redirect('HOME')
    capacity = 88
    current = Visitors.objects.filter(location='RCH').aggregate(Sum('count'))['count__sum']
    total_today = Visitors.objects.filter(location='RCH').filter(timestamp__date=timezone.now()).filter(count__gte=0).aggregate(Sum('count'))['count__sum']
    return render(request, 'visitors/index.html',{'location':'RCH', 'current':current, 'capacity':capacity, 'total_today':total_today})

def ddo(request):
    #IF USER IS NOT AUTHENTICATED SEND THEM HOME!
    if not request.user.is_authenticated:
        return redirect('HOME')
    capacity = 999
    current = Visitors.objects.filter(location='DDO').aggregate(Sum('count'))['count__sum']
    total_today = Visitors.objects.filter(location='DDO').filter(timestamp__date=timezone.now()).filter(count__gte=0).aggregate(Sum('count'))['count__sum']
    return render(request, 'visitors/index.html',{'location':'DDO', 'current':current, 'capacity':capacity, 'total_today':total_today})

def test(request):
    #IF USER IS NOT AUTHENTICATED SEND THEM HOME!
    if not request.user.is_authenticated:
        return redirect('HOME')
    capacity = 999
    current = Visitors.objects.filter(location='TEST').aggregate(Sum('count'))['count__sum']
    total_today = Visitors.objects.filter(location='TEST').filter(timestamp__date=timezone.now()).filter(count__gte=0).aggregate(Sum('count'))['count__sum']
    return render(request, 'visitors/index.html',{'location':'TEST', 'current':current, 'capacity':capacity, 'total_today':total_today})





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
        if count > 10:
            count = 10
        if count <-10:
            count = -10
    except:
        return redirect('/visitors/test')

    ##############################
    if count != 0 :
        Visitors(timestamp=timezone.now(),flr_email=flr_email,count=count,location=location).save()

    return redirect('/visitors/' + location.lower() + '/')






def VISITORS(request, location=''):
    #IF USER IS NOT AUTHENTICATED SEND THEM HOME!
    if not request.user.is_authenticated:
        return redirect('HOME')
    # HARDCODED STUFF - LOCATION
    if location.strip() == '' or location.upper() not in ['IRC','TRC','RCH','DDO','TEST']:
        return redirect('HOME')
    else:
        location = location.upper()
    #HARDCODED
    capacity = {'IRC':70,'TRC':92,'RCH':88,'DDO':999,'TEST':999}[location]
    current = Visitors.objects.filter(location=location).aggregate(Sum('count'))['count__sum']
    total_today = Visitors.objects.filter(location=location).filter(timestamp__date=timezone.now()).filter(count__gte=0).aggregate(Sum('count'))['count__sum']

    render_dict = {
        'capacity': {'IRC':70,'TRC':92,'RCH':88,'DDO':999,'TEST':999}[location],
        'location' : location,
        'current' : Visitors.objects.filter(location=location).filter(timestamp__date=timezone.now()).aggregate(Sum('count'))['count__sum'],
        'total_today' : Visitors.objects.filter(location=location).filter(timestamp__date=timezone.now()).filter(count__gte=0).aggregate(Sum('count'))['count__sum']
    }
    print(timezone.now())
    return render(request, 'visitors/index.html',render_dict)


def TESTER2(request, message=''):
    return redirect('TESTER1', message='YOLOMF')
