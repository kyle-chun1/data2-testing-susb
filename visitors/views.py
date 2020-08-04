from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseNotFound, JsonResponse

# Create your views here.

from visitors.models import Visitors
from django.db.models import Sum

def irc(request):
    try:
        default_email = request.GET['default_email']
    except:
        default_email = ''
    current = Visitors.objects.filter(location='IRC').aggregate(Sum('count'))['count__sum']
    return render(request, 'visitors/index.html',{'location':'IRC', 'default_email': default_email, 'current':current})

def trc(request):
    try:
        default_email = request.GET['default_email']
    except:
        default_email = ''
    current = Visitors.objects.filter(location='TRC').aggregate(Sum('count'))['count__sum']
    return render(request, 'visitors/index.html',{'location':'TRC', 'default_email': default_email, 'current':current})

def rch(request):
    try:
        default_email = request.GET['default_email']
    except:
        default_email = ''
    current = Visitors.objects.filter(location='RCH').aggregate(Sum('count'))['count__sum']
    return render(request, 'visitors/index.html',{'location':'RCH', 'default_email': default_email, 'current':current})

def ddo(request):
    try:
        default_email = request.GET['default_email']
    except:
        default_email = ''
    current = Visitors.objects.filter(location='DDO').aggregate(Sum('count'))['count__sum']
    return render(request, 'visitors/index.html',{'location':'DDO', 'default_email': default_email, 'current':current})

def test(request):
    try:
        default_email = request.GET['default_email']
    except:
        default_email = ''
    current = Visitors.objects.filter(location='TEST').aggregate(Sum('count'))['count__sum']
    return render(request, 'visitors/index.html',{'location':'TEST', 'default_email': default_email, 'current':current})




from visitors.models import Visitors
from django.utils import timezone

def submit(request):  #ASUME LOCATIONS ARE CORRECT
    print(str(request.POST['location']))
    if 'location' in request.POST and str(request.POST['location']) not in ['IRC','TRC','DDO','RCH','TEST']:
        location = 'TEST'
    else:
        location = request.POST['location']

    try:
        flr_email = request.POST['flr_email']
        count = int(request.POST['count'])
        if count > 5:
            count = 5
        if count <-5:
            count = -5
    except:
        return redirect('/visitors/test')

    x = Visitors(timestamp=timezone.now(),flr_email=flr_email,count=count,location=location).save()

    return redirect('/visitors/' + location.lower() + '?default_email=' + flr_email)
