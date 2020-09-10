from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
# Create your views here.

from shopify.models import AceInventoryList

################FUNCTION IMPORTS
from .functions import acetap_function

########## /shopify/acetap/?s=   RETURNS A JSON IF EXISTS
def acetap(request):
    if 's' in request.GET and request.GET['s'].strip() != '':
        try:
            return JsonResponse( acetap_function(request.GET['s'].strip())  )
        except:
            pass
    if 'u' in request.GET and request.GET['u'].strip() != '':
        try:
            if request.GET['u'].strip().split('/')[-1] != '':
                print()
                return JsonResponse( acetap_function( request.GET['u'].strip().split('/')[-1]) )
        except:
            pass

    return HttpResponseNotFound('NOT FOUND ON ACEHARDWARE.COM')






###################### QUEUED ENDPOINT
def queued(request):
    return_dict = {'count': 0, 'barcodes': []}
    query =  AceInventoryList.objects.filter(Status='QUEUED')
    return_dict['count'] = len(query)
    for i in query:
        return_dict['barcodes'].append(i.Upc)

    return JsonResponse(return_dict)


############################################
######LOOKUP VIEW - Write All codes to Database


def lookup(request):
    from shopify.functions import rch_post_shopify
    # ASSUME A BLANK SUBMISSION
    Title = ''
    Message = ''
    Color = ''
    Price = ''

    if 'barcode' in request.GET and str(request.GET['barcode']).strip()!='':
        Upc = request.GET['barcode']
        query = AceInventoryList.objects.filter(Upc=Upc)
        if len(query):
            Price = '$ ' +str(query[0].Retail)
            Title = query[0].Title
            if query[0].Status == 'minimal' or query[0].Status == 'ADDED':
                Color = 'text-success'
                Message = '[Status: Listed and Scanable in POS]'
            else:
                Color = 'text-primary'
                #ADD THIS TO QUEUED IF IT IS A ZERO
                if query[0].Status == 'zero' or query[0].Status == 'QUEUED':
                    query[0].Status = 'QUEUED'
                    query[0].save()
                    Message = '[Status: Not listed, has been queued for listing]'
                    add_result = rch_post_shopify(query[0].Index)
                    if add_result:
                        Message = 'Status: Product has just been listed - Thanks for scanning!'
                        query[0].Status = 'ADDED'
                        query[0].save()
        else:
            Price = 'NOT FOUND'
            Color = 'text-dark'
            Title = '<a id="message" target="_blank" href="https://google.com/search?q='+ Upc +'">GOOGLE SEARCH IT FOR PRICES</a>'
    return render(request,'shopify/lookup.html', {'Title':Title,'Message':Message,'Price':Price,'Color':Color})






############################
#RETURNBARCODE Function
#### NEEDS TO BE REWRITTEN


import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from shopify.functions import rch_barcode_generator

def barcodetest(request):
# open('', 'rb')
    try:
        BARCODE = request.GET['barcode']
        TITLE = request.GET['title']
        PRICE = request.GET['price']
        QUANTITY = int(request.GET['quantity'])
        if QUANTITY < 1:
            QUANTITY = 1
    except:
        return HttpResponseNotFound('Invalid Barcode')
    X = rch_barcode_generator(PRICE,BARCODE,TITLE,QUANTITY)
    # return HttpResponse(x)
    return FileResponse(X, as_attachment=False, filename="barcode.pdf")





#########################################
####RCHBARCODETEST VIEW
#*******************************************************************
#THIS IS THE PAGE THAT LOADS (NEED TO SEND THE JS OBJECT HERE)
from shopify.models import InventoryLookup as L
def rchbarcodetest(request):

    #IF USER IS NOT AUTHENTICATED SEND THEM HOME!
    if not request.user.is_authenticated:
        return redirect('HOME')


    the_dict = {}
    LIST = ['99900000','99800000','99700000','99600000',  '99500000','99300000','99200000','99100000','98900000',     '98800000','98600000']
    for i in LIST:
        BARCODES = L.objects.filter(handle=i)
        HANDLE = BARCODES[0]
        BARCODES_DICT = {}
        for j in BARCODES:
            if j.barcode != '':
                BARCODES_DICT[j.barcode] = j.option1
        the_dict[i] = {
            'title': HANDLE.title,
            'body_html':HANDLE.body_html,
            'tag-color': '',
            'barcodes':BARCODES_DICT,
        }


    return render(request,'shopify/rchbarcodetest.html',{'JSONOBJECT': json.dumps(the_dict) })












#THIS IS THE PRINTER FUNCTION!

from shopify.models import InventoryLookup
import json
from django.utils import timezone
from local_settings import S_URL
import requests
from shopify.models import InventoryMovement

def rchbarcodesubmissiontest(request):
    #Need to get BARCODE, QUANTITY, UPDATE(0/1)
    #Step 1 : This is where the decision happens !  If
    try:
        BARCODE = request.GET['barcode']
        QUANTITY = int(request.GET['quantity'])
        UPDATE = bool(int(request.GET['update']))   #0 or 1

        X = InventoryLookup.objects.get(barcode=BARCODE)


        if QUANTITY > 10:
            QUANTITY = 10
        elif QUANTITY <1:         ########## NEEDS TO BE CHANGED IN ALPHA to allow negetive inventory
            QUANTITY = 1

        ############UPDATE INVENTORY PART
        if UPDATE:
            the_request = requests.post(S_URL+'inventory_levels/adjust.json',json={'inventory_item_id': X.inventory_item_id,'location_id' : '45063176332','available_adjustment': QUANTITY,})
            the_dict = {
                'timestamp' : timezone.now(),
                'handle' : X.handle,
                'barcode' : X.barcode,
                'title' : X.title,
                'option1': X.option1,
                'product_id': X.product_id,
                'variant_id': X.variant_id,
                'compare_at_price' : X.compare_at_price,
                'inventory_item_id' : X.inventory_item_id,
                'product_type' : X.product_type,
                'vendor' : X.vendor,
                'sku' : X.sku,

                'staff' : 'chris@fingerlakesreuse.org.',  #############HARCODED
                'meta' : the_request.text,
                'location_id' : '45063176332',  ########HARCODED Reuse Community Hardware
                'quantity' : QUANTITY,
            }

            xx = InventoryMovement(**the_dict).save()
        #Update the DB and save a record of this transaction


    except:
        Y = rch_barcode_generator('INVALID','00000000','INVALID',1)
        return FileResponse(Y, as_attachment=False, filename="barcode.pdf")

    #Check is the Title begins with a $, if yes then DON't ATTACH NAME,  if its doensn't begin with $, then name first
    if X.option1[0] == '$':
        TITLE = f'{X.title}'
    else:
        TITLE = f'{X.option1}'
    Y = rch_barcode_generator('$'+ f'{X.compare_at_price:.2f}' ,X.barcode,TITLE,QUANTITY)

    return FileResponse(Y, as_attachment=False, filename="barcode.pdf")

#########################################
