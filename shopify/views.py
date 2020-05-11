from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
# Create your views here.

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
