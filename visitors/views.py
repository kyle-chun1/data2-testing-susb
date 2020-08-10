from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseNotFound, JsonResponse

# Create your views here.

from visitors.models import Visitors
from django.db.models import Sum

from visitors.functions import useastern,useastern_start, useastern_end

import pytz
from datetime import datetime
import pandas as pd

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



    Visitors_here_today = Visitors.objects.filter(
        location=location,
        timestamp__range=(useastern_start(),useastern_end())
        )

    ################# Section to Make the Hours Box at the bottom
    hours_dict = {}
    for i in Visitors_here_today:  #######ALSO TESTS FOR POSITIVE COUNTS!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        the_hour_str = useastern(i.timestamp).strftime("%I %p --")
        if i.count > 0:  ########### IMPORTANT : FILTER OUT ZEROS!
            if the_hour_str in hours_dict:
                hours_dict[the_hour_str] += i.count
            else:
                hours_dict[the_hour_str] = i.count
    print(hours_dict)
    # THIS OUTPUT THE HTML TABLE!
    info = pd.DataFrame([{'Hour of Day (Today)': i, 'Total Visitors that Entered': hours_dict[i]}  for i in hours_dict ])
    info = info.to_html(index=False,classes="text-center table table-sm")
    info = info.replace("right;", "center;")
    ################# INFOSECTION GET HOURLY DATA

    render_dict = {
        'capacity': {'IRC':70,'TRC':92,'RCH':88,'DDO':999,'TEST':999}[location],
        'location' : location,

        'current' : Visitors_here_today.aggregate(Sum('count'))['count__sum'],
        'total_today' : Visitors_here_today.filter(count__gte=0).aggregate(Sum('count'))['count__sum'],
        'info': info,
    }

    return render(request, 'visitors/index.html',render_dict)
