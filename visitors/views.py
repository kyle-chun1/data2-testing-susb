from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseNotFound, JsonResponse

# Create your views here.

from visitors.models import Visitors
from django.db.models import Sum, Count, DateTimeField
from django.db.models.functions import Trunc, Extract

from visitors.functions import useastern,useastern_start, useastern_end, start_end_date

import pytz
import json
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
    if location.strip() == '' or location.upper() not in ['IRC','TRC','RCH','DDO','TEST', '700-CABOOSE','TRC-DONATIONS']:
        return redirect('HOME')
    else:
        location = location.upper()



    start_date,end_date = start_end_date(request.GET)

    # Segment 1 : The Pivot table for the chart  ############################
    QUERY_1 = Visitors.objects.filter(location=location, count__gte=0, timestamp__range=(start_date,end_date)) \
        .annotate( tr_hour =Trunc('timestamp',kind='hour', tzinfo=pytz.timezone('US/Eastern'))) \
        .values('tr_hour').annotate(tr_hour_sum=Sum('count'))

    try:
        df = pd.DataFrame(data=list(QUERY_1),columns=list(QUERY_1[0].keys()))
        df['hour'] = df['tr_hour'].dt.hour
        df['date'] = df['tr_hour'].dt.date
        df_1 = df.pivot(index='date',columns='hour',values='tr_hour_sum'  ).fillna('')

    except:
        df_1 = pd.DataFrame(columns=['No Table Data in this range'])

    finally:
        # RETURN THE TABLE TO THE USER IF NEEDED !!!!!!!!!!!!!!!
        # PARSER SECTION
        if 'download' in request.GET:
            if request.GET['download'] == 'CSV':
                # PANDAS MANUAL RETURN THE OBJECT!
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename=raw_data_export.csv'
                df_1.to_csv(path_or_buf=response)
                return response

        df_1_html = df_1.to_html(classes='table table-sm table-striped text-center')



    # Segment 2 : the BAR CHART by DAY OF WEEK  ############################
    QUERY_2 = Visitors.objects.filter(location=location, count__gte=0, timestamp__range=(start_date,end_date)) \
        .annotate(week_day_number = Extract('timestamp','week_day', tzinfo=pytz.timezone('US/Eastern'))) \
        .values('week_day_number').annotate(week_day_sum=Sum('count')).order_by('week_day_number')

    weekday_list = { 1:'Sunday', 2:'Monday', 3:'Tuesday', 4:'Wednesday', 5:'Thursday', 6:'Friday', 7:'Saturday'}

    chartJS_2 = {
                'type': 'bar',
                'data': {
                    'labels': [weekday_list[x['week_day_number']] for x in list(QUERY_2)],
                    'datasets': [{
                        'label': 'Visitor Total by WEEKDAY',
                        'data': [x['week_day_sum'] for x in QUERY_2],
                        'backgroundColor': 'rgba(0, 120, 0, 0.85)',
                        'borderWidth': 1
                    }]
                },
                'options': {
                    'scales': {
                        'yAxes': [{
                            'ticks': {
                                'beginAtZero': True
                            }
                        }]
                    }
                }
            }





    # Segment 3 : bar chart hour of the day  ############################

    QUERY_3 = Visitors.objects.filter(location=location, count__gte=0, timestamp__range=(start_date,end_date)) \
        .annotate(hour_number = Extract('timestamp','hour', tzinfo=pytz.timezone('US/Eastern'))) \
        .values('hour_number').annotate(hour_sum=Sum('count')).order_by('hour_number')


    chartJS_3 = {
                'type': 'bar',
                'data': {
                    'labels': [x['hour_number'] for x in list(QUERY_3)],
                    'datasets': [{
                        'label': 'Visitor Total by HOUR',
                        'data': [x['hour_sum'] for x in QUERY_3],
                        'backgroundColor': 'rgba(84,100,191,0.85)',
                        'borderWidth': 1
                    }]
                },
                'options': {
                    'scales': {
                        'yAxes': [{
                            'ticks': {
                                'beginAtZero': True
                            }
                        }]
                    }
                }
            }

    # Segment 4 : bar chart MONTHLY AGGREGATION  ############################

    QUERY_4 = Visitors.objects.filter(location=location, count__gte=0, timestamp__range=(start_date,end_date)) \
        .annotate(month_number = Extract('timestamp','month', tzinfo=pytz.timezone('US/Eastern'))) \
        .values('month_number').annotate(month_sum=Sum('count')).order_by('month_number')

    month_list = { 1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}

    chartJS_4 = {
                'type': 'bar',
                'data': {
                    'labels': [ month_list[ x['month_number'] ] for x in list(QUERY_4)],
                    'datasets': [{
                        'label': 'Visitor Total by MONTH',
                        'data': [x['month_sum'] for x in QUERY_4],
                        'backgroundColor': 'rgba(242,170,82,0.85)',
                        'borderWidth': 1
                    }]
                },
                'options': {
                    'scales': {
                        'yAxes': [{
                            'ticks': {
                                'beginAtZero': True
                            }
                        }]
                    }
                }
            }


    # Render section :::::::::
    start_date_f = start_date.strftime('%Y-%m-%d')
    end_date_f = end_date.strftime('%Y-%m-%d')

    return_dict = {
        'start_date' : start_date_f,
        'end_date' : end_date_f,
        'table' : df_1_html,
        'location': location,
        'download_csv_link' : f'?download=CSV&start={start_date_f}&end={end_date_f}',
        'chartJS_2' : json.dumps(chartJS_2),
        'chartJS_3' : json.dumps(chartJS_3),
        'chartJS_4' : json.dumps(chartJS_4),
    }
    return render(request,'visitors/hourly.html',return_dict)
