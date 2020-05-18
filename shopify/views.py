from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
# Create your views here.

from shopify.models import AceInventoryList

################FUNCTION IMPORTS
from .functions import acetap_function,test_function

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



##########
#TESTER view
# def test(request):
#     the_params = {
#     'fields':'id',
#     'limit':1,
#     'vendor':'dont_use_ace',
#     }
#     x = test_function('products.json',the_params,'products')
#     return HttpResponse(x)
#        # return HttpResponse(test_function('products.json',{'fields':'id','page_info':'eyJsYXN0X2lkIjo0OTc0MjE5Mjk2OTA4LCJsYXN0X3ZhbHVlIjoiNCBlbGVtZW50YXJ5IHNjaG9vbCBGSUNUSU9OIEJPT0tTLCBjaGFwdGVyIGJvb2tzLCBNYXR0IENocmlzdG9waGVyIiwiZGlyZWN0aW9uIjoibmV4dCJ9'}))

def test(request):
    the_params = {
    'fields':'id',
    'limit':250,
    }
    x = test_function('products.json',the_params,'products')
    return HttpResponse(x)
       # return HttpResponse(test_function('products.json',{'fields':'id','page_info':'eyJsYXN0X2lkIjo0OTc0MjE5Mjk2OTA4LCJsYXN0X3ZhbHVlIjoiNCBlbGVtZW50YXJ5IHNjaG9vbCBGSUNUSU9OIEJPT0tTLCBjaGFwdGVyIGJvb2tzLCBNYXR0IENocmlzdG9waGVyIiwiZGlyZWN0aW9uIjoibmV4dCJ9'}))




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
    # ASSUME A BLANK SUBMISSION
    Title = ''
    Message = ''
    Color = ''
    Price = ''

    if 'barcode' in request.POST and str(request.POST['barcode']).strip()!='':
        Upc = request.POST['barcode']
        query = AceInventoryList.objects.filter(Upc=Upc)
        if len(query):
            Price = '$ ' +str(query[0].Retail)
            if query[0].Status == 'minimal' or query[0].Status == 'ADDED':
                Color = 'text-success'
                Title = query[0].Title
                Message = '[Status: Listed]'
            else:
                Color = 'text-primary'
                Title = query[0].Title
                Message = '[Status: Not listed, but will be listed soon!]'
                #ADD THIS TO QUEUED IF IT IS A ZERO
                if query[0].Status == 'zero':
                    print('Needs to be FLAGGED FOR QUEUE')
                    query[0].Status = 'QUEUED'
                    query[0].save()
        else:
            Price = 'NOT FOUND'
            Color = 'text-dark'
            Title = '<a id="message" target="_blank" href="https://google.com/search?q='+ Upc +'">GOOGLE SEARCH IT FOR PRICES</a>'
    return render(request,'shopify/lookup.html', {'Title':Title,'Message':Message,'Price':Price,'Color':Color})
