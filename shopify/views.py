from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
# Create your views here.

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
