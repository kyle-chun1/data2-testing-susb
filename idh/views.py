from django.shortcuts import render
# from django.http import HttpResponse
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool

from .models import ddo_hourly

from datetime import datetime

# Create your views here.
def idh(request):
    ###Step 1 : Determine if the Date values are valid and acceptable. (Swap them if mixed in range)
    flag = False
    if 'start' in request.GET and 'end' in request.GET:
        if request.GET['start'] != '' and request.GET['end'] != '':
            try:
                start_date = datetime.strptime(request.GET['start'], '%Y-%m-%d')
                end_date = datetime.strptime(request.GET['end'], '%Y-%m-%d')
                flag = True
                if start_date > end_date:
                        start_date, end_date = end_date , start_date
            except:
                pass

    ###Step 2 : If they are valid then pass them to the list, if not generate default starting from this month
    if not flag:
        start_date=datetime.now().replace(day=1)
        end_date = datetime.now()

    ### Step 3 : Crunch the start_date and end_date to strings for Django Date Range + html output
    start_date = datetime.strftime(start_date,'%Y-%m-%d')
    end_date = datetime.strftime(end_date,'%Y-%m-%d')


# BOKEH EXPERIMENT#############################################################################
    # plot=figure()
    # plot.circle(['h01','h02','h03'],[2,3,5],size=10,color="blue")
    # (script, div) = components(plot)
    d = ddo_hourly.objects.filter(hDate__range=[start_date , end_date])
    fruits = [str(x.hDate) for x in d]
    counts = [x.hTotal for x in d]
    # fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
    # counts = [5, 3, 4, 2, 4, 6]
    p1 = figure(x_range=fruits, plot_width=1000, title='')
    # p.line([i for i,x in enumerate(d)],[y.hTotal for y in d], line_width=1, color='red')
    p1.vbar(x=fruits, top=counts, width=0.75)
    p1.xgrid.grid_line_color = None
    p1.y_range.start = 0
    p1.xaxis.major_label_orientation = "vertical"
    (script1, div1) = components(p1)

# BOKEH EXPERIMENT#############################################################################


    # RETURN PART

    message_text = str(flag)
    return render(request,'idh.html',{
    'script1' : script1,
    'div1' : div1,
    'message_text' : str(start_date) + '\n' + str(end_date),
    'start_date' : start_date,
    'end_date' : end_date,
    'max_date' : datetime.strftime(datetime.now(),'%Y-%m-%d')
    })
