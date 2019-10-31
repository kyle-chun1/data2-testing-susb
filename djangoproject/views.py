from django.http import HttpResponse
from django.shortcuts import render
from django.utils.timezone import datetime

def mm(request):


    return_dict = {'tDate':str(datetime.today())[0:10]}

    return  render(request, 'material.html',return_dict)

    # return HttpResponse()


def temp(request):
    if request.method == 'POST':
        mFormData = {
        'mName' : request.POST['mName'],
        'mDate' : request.POST['mDate'],
        'mMode' : request.POST['mMode'],
        'mOrigin' : request.POST['mOrigin'],
        'mOriginLocation' : request.POST['mOriginLocation'],
        'mDestination' : request.POST['mDestination'],
        'mDestinationLocation' : request.POST['mDestinationLocation'],
        'mMaterial' : request.POST['mMaterial'],
        'mHidden' : request.POST['mHidden'],
        }
        x=''
        for i,j in mFormData.items():
            x = x + i + ' : ' + j +  '<br><br>'
    else:
        x = '<h1>NOT POSTED FORM</h1>'
    return HttpResponse(x)
