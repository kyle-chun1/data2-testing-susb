from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, FileResponse


from pricing.functions import barcode_reuse_1

from pricing.models import *
import json



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
    if location.upper() in ['TRMC', 'TRC', 'TRMC']:
        location = 'trmc'
    else:
        return(redirect('/'))

    #MESSAGE CHECK
    # if 'message' in request.session and request.session['message'] == 'success':
    #     message = 'SUCCESS'
    #     request.session['message'] = ''
    # else:
    #     request.session['message'] = ''
    #     message='Glenn'

    products_std = [i.shopify_handle for i in Product.objects.filter(classifier__in=['W','R','G','B','Y','L','O'])]
    products_unit = {}
    V = Variant.objects.filter(product__classifier='U').values('variant','title','price')

    for i in V:
        try:
            if i['variant'][0].upper() != 'K':
                products_unit[i['variant'][0:5]].append([ i['variant'],i['title'],f"{i['price']:.2f}" ])
        except:
            products_unit[i['variant'][0:5]] = list()


    return render(request, 'pricing/pricing_trmc.html',{'products_std': products_std, 'products_unit':products_unit})






def pricing_submit(request):
    #authentication
    if not request.user.is_authenticated:
        return redirect('HOME')

    if 1==1:
        VARIANT = request.GET['variant']
        PRINT = bool(int(request.GET['print']))
        INVENTORY = bool(int(request.GET['inventory']))
        QUANTITY = int(request.GET['quantity'])

        color_reference = {'W':'WHITE','U':'WHITE (Unit)', 'R':'RED', 'B':'BLUE', 'Y':'YELLOW', 'G':'GREEN', 'O':'ORANGE', 'L':'LAVENDER'}

        V = Variant.objects.get(variant=VARIANT)

        if V.title[0] == '$':
            TITLE = V.product
        else:
            TITLE = V.title

        X = barcode_reuse_1(VARIANT, V.price, V.title, color_reference[V.variant[0]], 'G I J E', QUANTITY)
        return FileResponse(X, as_attachment=False, filename="barcode.pdf")


    # barcode_reuse_1(VARIANT,PRICE,TITLE, COLOR, HANDLE, QUANTITY)
