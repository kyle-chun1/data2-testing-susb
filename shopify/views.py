from django.shortcuts import render
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
