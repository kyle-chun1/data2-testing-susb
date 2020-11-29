from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseNotFound, JsonResponse

# Create your views here.

from visitors.models import Visitors
from django.db.models import Sum, Count, DateTimeField
from django.db.models.functions import Trunc

from visitors.functions import useastern,useastern_start, useastern_end, start_end_date

import pytz
from datetime import datetime
import pandas as pd

from visitors.models import Visitors
from django.utils import timezone


from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool, ColumnDataSource, ranges, LabelSet



def submit(request):  #ASUME LOCATIONS ARE CORRECT
    #IF USER IS NOT AUTHENTICATED SEND THEM HOME!
    if not request.user.is_authenticated:
        return redirect('HOME')

# HARCOCDED LOCATIONS!!!!!!!!!!!!!!!!
    if 'location' in request.POST and str(request.POST['location']) not in ['IRC','TRC','DDO','RCH','TEST', '700-CABOOSE']:
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
    if location.strip() == '' or location.upper() not in ['IRC','TRC','RCH','DDO','TEST', '700-CABOOSE']:
        return redirect('HOME')
    else:
        location = location.upper()
    #HARDCODED
    capacity = {'IRC':70,'TRC':92,'RCH':88,'DDO':999,'TEST':999, '700-CABOOSE': 35}[location]



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
        'capacity': {'IRC':70,'TRC':92,'RCH':88,'DDO':999,'TEST':999,'700-CABOOSE': 35}[location],
        'location' : location,

        'current' : Visitors_here_today.aggregate(Sum('count'))['count__sum'],
        'total_today' : Visitors_here_today.filter(count__gte=0).aggregate(Sum('count'))['count__sum'],
        'info': info,
    }

    for i in Visitors_here_today:
        print(useastern(i.timestamp), i.count)

    return render(request, 'visitors/index.html',render_dict)










###########################################################################
# ALL STORES CAPCTITY VIEW - 3 Column charset
def capacity(request):

    try:
        GET_start = datetime.strptime(request.GET['start'], "%Y-%m-%d")
        start = useastern().replace(year=GET_start.year, month=GET_start.month, day=GET_start.day)

    except:
        start = useastern()

    start_date = start.strftime("%Y-%m-%d")  # DONE FOR PARSING IT TO THE HTML START DATE


    V = Visitors.objects.filter(timestamp__range=(useastern_start(start),useastern_end(start))).order_by('timestamp')


    p = figure(plot_width=1200, plot_height=600,x_axis_type="datetime")

    locations = {'IRC':'green','TRC':'blue','RCH':'red', '700-CABOOSE': 'black'}
    capacities = {'IRC':70,'TRC':92,'RCH':88, '700-CABOOSE':35}
    for location in locations:
        x = [useastern(x.timestamp) for x in V.filter(location=location)]
        y = [y.count for y in V.filter(location=location)]
        running_sum = 0
        Y = []
        for i in y:
            running_sum += i
            Y.append(running_sum/capacities[location]*100)
        p.line(x,Y,color=locations[location],line_width=4,line_alpha=0.5,legend_label=location)

    p.legend.click_policy="hide"
    p.xaxis.axis_label = 'Time of Day'
    p.yaxis.axis_label = 'Percentage (%) of Capacity Reached'
###############RENDER PART


    # p.patch([1, 2, 3, 4, 5], [6, 7, 8, 7, 3], alpha=0.5, line_width=2, color="#FF0000")
    # p.line(x,y, color='#000000')

    allstores_bokeh_script, allstores_bokeh_html = components(p)

    render_dict = {
        'allstores_bokeh_script' : allstores_bokeh_script,
        'allstores_bokeh_html': allstores_bokeh_html,
        'start_date': start_date,
    }
    return render(request,'visitors/capacity.html',render_dict)




###########################################################################
# visitors_hourly VIEW - HOURLY STATISTICS
# v2.0

def visitors_hourly(request, location=''):

    #IF USER IS NOT AUTHENTICATED SEND THEM HOME!
    if not request.user.is_authenticated:
        return redirect('HOME')
    # HARDCODED STUFF - LOCATION
    if location.strip() == '' or location.upper() not in ['IRC','TRC','RCH','DDO','TEST', '700-CABOOSE']:
        return redirect('HOME')
    else:
        location = location.upper()



    start_date,end_date = start_end_date(request.GET)


    QUERY = Visitors.objects.filter(location=location, count__gte=0, timestamp__range=(start_date,end_date)).annotate(ha_hour=Trunc('timestamp',kind='hour',tzinfo=pytz.timezone('US/Eastern'))).values('ha_hour').annotate(ha_sum=Sum('count'))


    df = pd.DataFrame(columns=['ha_hour','ha_sum'])

    for i in QUERY:
        df = df.append(i,ignore_index=True)

    df['hour'] = df['ha_hour'].dt.hour
    df['date'] = df['ha_hour'].dt.date

    return_dict = {
        'start_date' : start_date.strftime('%Y-%m-%d'),
        'end_date' : end_date.strftime('%Y-%m-%d'),
        'table' : df.pivot(index='date',columns='hour',values='ha_sum'  ).fillna('').to_html(),
        'location': location,
    }
    return render(request,'visitors/hourly.html',return_dict)
