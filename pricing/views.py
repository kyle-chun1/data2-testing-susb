from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, FileResponse
from django.db.models import Sum
from django.db.models.functions import Trunc

from pricing.functions import barcode_reuse_1

from pricing.models import *
import json

from datetime import datetime, timedelta
import pytz


# Create your views here.
def tester2(request, x=1):
    for i in range(20): print(request.session.get('msg','DEFAULT'))
    request.session['msg'] = None
    return render(request,'pricing/pricing_trmc.html', {})


##########
def tester3(request):
    Y = barcode_reuse_1('WTBMM1500',1500,'Building Materials', 'WHITE', 'WTBMM', 2)
    request.session['message'] = 'success'
    return FileResponse(Y, as_attachment=False, filename="barcode.pdf")

def tester_main(request, yolo=1):
    if 1==1:
        request.session['msg'] = 'GOOOOOOGLE'
        return redirect(reverse('pricing:tester2'))
    return render(request, 'pricing/tester_main.html', {})

def tester_submit(request):
    HttpResponse('SUBMITTED')
##########




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

    #MESSAGE CHECK
    # if 'message' in request.session and request.session['message'] == 'success':
    #     message = 'SUCCESS'
    #     request.session['message'] = ''
    # else:
    #     request.session['message'] = ''
    #     message='Glenn'

    products_std = [i.shopify_handle for i in Product.objects.filter(location=Location.objects.get(location=LOCATION), classifier__in=['W','R','G','B','Y','L','O'])]
    products_unit = {}
    V = Variant.objects.filter(product__location=Location.objects.get(location=LOCATION), product__classifier='U').values('variant','title','price')

    for i in V:
        try:
            if i['variant'][0].upper() != 'K':
                products_unit[i['variant'][0:5]].append([ i['variant'],i['title'],f"{i['price']:.2f}" ])
        except:
            products_unit[i['variant'][0:5]] = list()


    if LOCATION=='T':
        return render(request, 'pricing/pricing_trmc.html',{'products_std': products_std, 'products_unit':products_unit})
    elif LOCATION == 'I':
        return render(request, 'pricing/pricing_irc.html',{'products_std': products_std, 'products_unit':products_unit})






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




#########
def my_pricing_table(request):
    if not request.user.is_authenticated:
        return redirect('HOME')

    response_html = '<table style="background:red"><thead><tr><th>Date/Time</th><th>Product</th><th>Variant</th><th>Price</th><th>Quantity</th></tr></thead><tbody>'

    QUERY = Pricing.objects.filter(staff_id=request.user.email.split('@')[0])\
        .order_by('-timestamp')[:10]\
        .values('variant__title','timestamp','variant__product__title','variant__price', 'quantity')

    for i in QUERY:
        response_html += f"<tr><td>{ datetime.strftime(i['timestamp'].astimezone(tz=pytz.timezone('US/Eastern')),'%a %b %d, %Y - %I:%M %p') }</td><td>{i['variant__product__title']}</td><td>{i['variant__title']}</td><td>{i['variant__price']}</td><td>{i['quantity']}</td>"


    response_html += f'</tbody></table>'
    return HttpResponse(response_html)







#################################
# START
#################################
def today(request):
    P = Pricing.objects.filter(timestamp__gte=yes, variant__product__location=Location.objects.get(location='T'), inventory=True)
    return HttpResponse('response_html')
