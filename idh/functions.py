import pandas as pd
from .models import ddo_hourly

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool
from bokeh.layouts import row

from datetime import timedelta


def import_records():
    df = pd.read_csv('test_data.csv')
    print(df.shape == df.isna().shape and df.shape == df.isnull().shape)
    df['hDate'] = pd.to_datetime(df['hDate'])
    temp_columns = list(df.columns)
    for i in range(0,df.shape[0]):
        temp_dict = {}
        the_total = 0
        for n,j in enumerate(df.iloc[i]):
            temp_dict[temp_columns[n]] = j
            if temp_columns[n] != 'hDate' : the_total += j
        temp_dict['hTotal'] = the_total
        ddo_hourly.objects.create(**temp_dict).save()


def bokeh_render_hours(q):
    #This functions takes in a queryset and returns a Bokeh Graph
    plot = figure(x_axis_label='Date Range', y_axis_label='Individual Donations', x_axis_type='datetime')
    
    x = [i.hDate for i in q]
    y = [i.hTotal for i in q]
    c = ['5A9D43' if i.hTotal < 100 else 'red' for i in q]
    
    # plot.circle([1,10,35,50],[1,2,3,4],size=20, color="blue")
    # plot.line(x=x,y=y, color='red')
    plot.vbar(x=x,top=y, width=timedelta(days=0.75), color=c)
    for i in q:
        print(vars(i))
    return row(plot,sizing_mode='scale_both')