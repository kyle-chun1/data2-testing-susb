from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, FileResponse
from django.db.models import Sum, Avg, Count, Min, Max, ExpressionWrapper, F, DecimalField, DateTimeField
from django.db.models.functions import Trunc, Extract

from pricing.functions import barcode_reuse_1, color_wheel_2021

from pricing.models import *
import json

from datetime import datetime, timedelta
from django.utils import timezone
import pytz

from visitors.functions import *

from visitors.functions import start_end_date

import pandas as pd


def pricing_portal(request, location):
    #authentication
    if not request.user.is_authenticated:
        return redirect('HOME')

    # LOCATION SLUG CHECK
    if location.upper() in ['TRMC', 'TRC', 'TRMC', 'RMC']:
        LOCATION = 'T'
    elif location.upper() in ['IRC', 'IRMC']:
        LOCATION = 'I'
    else:
        return(redirect('/'))



    products_std = [i.shopify_handle for i in Product.objects.filter(location=Location.objects.get(location=LOCATION), classifier__in=['W','R','G','B','Y','L','O'])]
    products_unit = {}
    V = Variant.objects.filter(product__location=Location.objects.get(location=LOCATION), product__classifier='U', visible=True).values('variant','title','price').order_by('title')


########################### FOCUS / BACKUP
    # for i in V:
    #     try:
    #         if i['variant'][0].upper() != 'K':
    #             products_unit[i['variant'][0:5]].append([ i['variant'],i['title'],f"{i['price']:.2f}" ])
    #     except:
    #         products_unit[i['variant'][0:5]] = list()
###########################

    # Create a SET of the unique IDS
    products_ids = set([x['variant'][0:5] for x in V])
    #Declare a blank Dict and Add the unique IDS to the dict with empty lists()
    products_unit_test = {}
    for i in products_ids:
        products_unit_test[i] = list()

    for i in V:
        products_unit_test[ i['variant'][:5] ].append([  i['variant'],i['title'],f"{i['price']:.2f}"  ])

########################### TEST SEGMENT END

    color_reference = {'W':'White', 'R':'Red', 'B':'Blue', 'Y':'Yellow', 'G':'Green', 'O':'Orange', 'L':'Lavender'}
    CC = color_wheel_2021(timezone.now())
    CColor = color_reference[CC]
    print(CC,CColor)

    if LOCATION=='T':
        return render(request, 'pricing/pricing_trmc.html',{'products_std': products_std, 'products_unit':products_unit_test, 'CColor' : CColor, 'CC': CC })  ###########FOLLOWUP : TESTING NEW FORMAT FOR DICT
    elif LOCATION == 'I':
        return render(request, 'pricing/pricing_irc.html',{'products_std': products_std, 'products_unit':products_unit_test, 'CColor' : CColor, 'CC': CC })






def pricing_submit(request):
    #authentication
    if not request.user.is_authenticated:
        return redirect('HOME')

    try:
        VARIANT = request.GET['variant']
        PRINT = bool(int(request.GET['print']))
        INVENTORY = bool(int(request.GET['inventory']))
        QUANTITY = int(request.GET['quantity'])

        color_reference = {'W':'WHITE','U':'WHITE (Unit)', 'R':'RED', 'B':'BLUE', 'Y':'YELLOW', 'G':'GREEN', 'O':'ORANGE', 'L':'LAVENDER'}

        V = Variant.objects.get(variant=VARIANT)

        if V.title[0] == '$':
            TITLE = str(V.product)
        else:
            TITLE = str(V.title)

        #Submit to DB!!!
        STAFF_ID = str(request.user.email).split('@fingerlakesreuse.org')[0]
        submission = Pricing.objects.create(variant=Variant.objects.get(variant=VARIANT), quantity=QUANTITY, staff_id=STAFF_ID, print=PRINT, inventory=INVENTORY)

        #GENERATE CODE
        X = barcode_reuse_1(VARIANT, V.price, TITLE, color_reference[V.variant[0]], ' '.join(VARIANT[:5]), QUANTITY)
        return FileResponse(X, as_attachment=False, filename="barcode.pdf")

    except:

        E = barcode_reuse_1('ERORR', 0, 'ERROR', 'ERROR', 'ERROR', 1)
        return FileResponse(E, as_attachment=False, filename="barcode-ERROR.pdf")

    # barcode_reuse_1(VARIANT,PRICE,TITLE, COLOR, HANDLE, QUANTITY)




########
def my_pricing_table(request):
    if not request.user.is_authenticated:
        return redirect('HOME')

    response_html = '<table id="mainTable" class="table table-sm"><thead><tr><th>ID</th><th>Date/Time</th><th>Tag</th><th>Product</th><th>Variant</th><th>Price</th><th>Quantity</th><th>DELETE</th></tr></thead><tbody>'
    classifier_choices = {'U':'Unit','W':'White','Y':'Yellow','R':'Red','O':'Orange','B':'Blue','G':'Green','L':'Lavender'}


    QUERY = Pricing.objects.filter(staff_id=request.user.email.split('@')[0], inventory=True, deleted=False)\
        .order_by('-timestamp')[:20]\
        .values('variant__product__classifier','variant__title','timestamp','variant__product__title','variant__price', 'quantity', 'id')

    for i in QUERY:
        # IF the timestamp is not less than a day old, render the delete button > so that folks can delete it if needed.
        if i['timestamp'] > timezone.now()-timedelta(days=1):
            delete_button_html = f'<a target="_new" href="{reverse("pricing:delete_record", kwargs={"record":i["id"]})}" class="btn btn-success btn-sm" role="button" aria-pressed="true">DEL</a>'
        else:
            delete_button_html = '-'
        response_html += f"<tr><td>{i['id']}</td><td>{datetime.strftime(i['timestamp'].astimezone(tz=pytz.timezone('US/Eastern')),'%a %d/%m/%y - %I:%M %p') }</td><td>{classifier_choices[i['variant__product__classifier']]}</td><td>{i['variant__product__title']}</td><td>{i['variant__title']}</td><td>{i['variant__price']}</td><td>{i['quantity']}</td><td>{delete_button_html}</td>"

    response_html += f'</tbody></table>'
    return HttpResponse(response_html)




def delete_record(request, record):
    if not request.user.is_authenticated:
        return redirect('HOME')

    R = Pricing.objects.filter(id=record)\
        .values('deleted','id','staff_id','timestamp','variant__variant', 'variant__product__product_type__product_type','quantity')[0]

    if R['staff_id'] != request.user.email.split('@')[0]:
        return HttpResponse('NOT YOUR USER ACCOUNT')

    if R['timestamp'] < timezone.now()-timedelta(days=1):
        return HttpResponse('THIS RECORD IS TOO OLD TO DELETE')


    return_dict = {'R':R}
    return render(request, 'pricing/delete_record.html', return_dict)




def delete_submit(request):
    try:
        record = int(request.POST.get('id'))
        print(record)

        R = Pricing.objects.filter(id=record)[0]
        print(vars(R))
        R.deleted = True
        R.save()
        return redirect( reverse('pricing:delete_record',kwargs={"record":record }) )
    except:
        return HttpResponse('ERROR OCCURED')

# ######### USE THIS FOR PRITING TAGS TEMPORARILY
# def temp_barcode(request):
#     E = barcode_reuse_1('K04F03:UTHOW1.00GE06',3.0,'Buy 4 for $3', 'BULK', 'HOUSEWARES', 1)
#     return FileResponse(E, as_attachment=False, filename="barcode-ERROR.pdf")


#################################
# START
#################################
def raw(request,location):
    #authentication
    if not request.user.is_authenticated:
        return redirect('HOME')

    # LOCATION SLUG CHECK
    if location.upper() in ['TRMC', 'TRC', 'TRMC', 'RMC']:
        LOCATION = 'T'
        location = 'TRMC'
    elif location.upper() in ['IRC', 'IRMC']:
        LOCATION = 'I'
        location = 'IRC'
    else:
        return(redirect('HOME'))

    #GET the GET values from the view or else generate them
    start_date, end_date = start_end_date(request.GET)

    P = Pricing.objects.filter(timestamp__gte=start_date, timestamp__lte=end_date ,variant__product__location=Location.objects.get(location=LOCATION), inventory=True, deleted=False)\
    .values('variant__variant').annotate(TOTAL_QUANTITY=Sum('quantity'), TOTAL_VALUE=ExpressionWrapper(Sum('quantity')*F('variant__price'), output_field=DecimalField())   )\
    .values('variant__variant','variant__product__product_type__product_type', 'variant__product__classifier', 'variant__product__title', 'variant__title', 'variant__price', 'TOTAL_QUANTITY', 'TOTAL_VALUE')






    return render(request, 'pricing/raw.html',{
        'location':location,
        'P': P,
        'start_date' : start_date.strftime('%Y-%m-%d'),
        'end_date' : end_date.strftime('%Y-%m-%d'),
    })




######### STATS PAGE  ##################
def stats(request, location=''):
    #authentication
    if not request.user.is_authenticated:
        return redirect('HOME')
    #GET the GET values from the view or else generate them
    start_date, end_date = start_end_date(request.GET)
    # LOCATION SLUG CHECK
    if location.upper() in ['TRMC', 'TRC', 'TRMC', 'RMC']:
        LOCATION = 'T'
        location = 'TRMC'
    elif location.upper() in ['IRC', 'IRMC']:
        LOCATION = 'I'
        location = 'IRC'
    else:
        return(redirect('HOME'))



    Qu = Pricing.objects.filter(timestamp__gte=start_date, timestamp__lte=end_date ,variant__product__location=Location.objects.get(location=LOCATION), inventory=True, deleted=False)\

    total_items = Qu.aggregate(total_items=Sum('quantity'))['total_items']
    total_pricing_value = Qu.aggregate(TOTAL_VALUE=Sum(ExpressionWrapper(F('quantity')*F('variant__price'), output_field=DecimalField())))['TOTAL_VALUE']
    items_per_submission = Qu.aggregate(items_per_submission=Avg('quantity'))['items_per_submission']

    #Product Type Breakdown
    PT = Qu.values('variant__product__product_type__product_type').annotate(
        PT = F('variant__product__product_type__product_type'),
        PRICING_VALUE = Sum(ExpressionWrapper(F('quantity')*F('variant__price'), output_field=DecimalField())),
        TOTAL_ITEMS = Sum('quantity'),
        COUNT = Count('variant__product__product_type__product_type'),
        ITEM_SUBMISSIONS = Avg('quantity'),
        AVG = Avg('variant__price'),
        CAT = F('variant__product__product_type__category__category'),
    )

    #Product Type Breakdown
    ST = Qu.values('staff_id').annotate(
        ST = F('staff_id'),
        PRICING_VALUE = Sum(ExpressionWrapper(F('quantity')*F('variant__price'), output_field=DecimalField())),
        TOTAL_ITEMS = Sum('quantity'),
        COUNT = Count('variant__product__product_type__product_type'),
        ITEM_SUBMISSIONS = Avg('quantity'),
        AVG = Avg('variant__price'),
    )
######################
# TRIED TO DO IT THE DJANGO-PIVOT WAY BUT FAILED, REVERTING TO PANDAS
    # DT = Qu.annotate(date=Trunc('timestamp', 'day', tzinfo=pytz.timezone('US/Eastern')),
    #     product_type=F('variant__product__product_type__product_type')).values('date','product_type').annotate(quantity_sum=Sum('quantity')).order_by('date')

    DT = Qu.annotate(date=Trunc('timestamp', 'day', tzinfo=pytz.timezone('US/Eastern')),
        product_type=F('variant__product__product_type__product_type')).values('date','product_type', 'quantity')

    for i in DT: print(i)
    ## PARSE IN TO PANDAS
    #
    # df = pd.DataFrame(DT, columns=['quantity','product_type','date'])



####################


    try:
        avg_item_price = total_pricing_value / total_items
    except:
        avg_item_price = ''

    return render(request, 'pricing/stats.html',{
        'location' : location,
        # 'P': P,
        'start_date' : start_date.strftime('%Y-%m-%d'),
        'end_date' : end_date.strftime('%Y-%m-%d'),
        'total_items' :  total_items,
        'total_pricing_value' : total_pricing_value,
        'pricing_submissions' : Qu.count(),
        'avg_item_price' : avg_item_price,
        'items_per_submission' : items_per_submission,
        'PT' : PT,
        'ST' : ST,
        'DT' : DT,

    })

######################
# NEW HOME > RENDERS THE LINKS FOR HOME  #TOVA

def template_home(request):
    L = Link.objects
    return_dict = {
        'L_Q' : L.filter(category='Q').order_by('order'),
        'L_A' : L.filter(category='A').order_by('order'),
        'L_C' : L.filter(category='C').order_by('order'),
        'L_E' : L.filter(category='E').order_by('order'),
    }
    return render(request, 'pricing/spark_base.html', return_dict)







#####################
# TESTER FOR NEW RETAIL RESOURCES

def tester(request):
    return render(request,'pricing/tester.html')
