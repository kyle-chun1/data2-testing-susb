from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.timezone import datetime
from .models import RawMaterialMovement, ExpandedMaterialMovement
import requests
import json
from .functions import ExpansionFunction


def mm(request):
    return_dict = {
        'tDate' : str(datetime.today())[0:10],
        'tTimestamp' : str(datetime.now().timestamp()),
        }
    return  render(request, 'mm/material.html',return_dict)
    # return HttpResponse()




def mmsubmit(request):
    if request.method == 'POST':

        mFormData = {
        'rName' : request.POST['mName'],
        'rDate' : request.POST['mDate'],
        'rMode' : request.POST['mMode'],
        'rTrips' : request.POST['mTrips'],
        'rOrigin' : request.POST['mOrigin'],
        'rOriginLocation' : request.POST['mOriginLocation'],
        'rDestination' : request.POST['mDestination'],
        'rDestinationLocation' : request.POST['mDestinationLocation'],
        'rMaterial' : request.POST['mMaterial'],
        'rHidden' : request.POST['mHidden'],
        'rTimestamp' : request.POST['mTimestamp'],
        }


        #Submit to the Django Database
        Submission = RawMaterialMovement(**mFormData)
        RawMaterialMovement.objects.create(**mFormData).save()



        # Create a text file
        with open('raw_log/' + str(mFormData['rTimestamp']) ,'w') as temp:
            temp.write(json.dumps(mFormData))


        # Submit to Google Sheets Redundancy
        googleurl = 'https://docs.google.com/forms/d/e/1FAIpQLSfXjO5RPjy9nz4M8x52CeVtaynOmXkd_3KnXtO6I3MHE3O0Aw/formResponse'
        googleparams = {
            'entry.2054024210' : mFormData['rName'],
            'entry.781229162' : mFormData['rDate'],
            'entry.540449382' : mFormData['rMode'],
            'entry.1201600051' : mFormData['rTrips'],
            'entry.1978589283' : mFormData['rOrigin'],
            'entry.392818040' : mFormData['rOriginLocation'],
            'entry.1847268034' : mFormData['rDestination'],
            'entry.745648505' : mFormData['rDestinationLocation'],
            'entry.2044658746' : mFormData['rMaterial'],
            'entry.1404056945' : mFormData['rHidden'],
            'entry.2092600452' : mFormData['rTimestamp'],
        }

        #GOOGLE FORM SUBMIT OFF
        googlerequest = requests.post(googleurl, data=googleparams)

        #THIS iS WHERE WE EXPAND STUFF


        # MESSAGE = ExpansionFunction(mFormData)
        for i in ExpansionFunction(mFormData):
            if str(mFormData['rHidden']).strip().lower() != 'test':
                ExpandedMaterialMovement.objects.create(**i).save()


        # MESSAGE = RawMaterialDict


        return render(request, 'mm/submission.html',{'message':Submission })

    else:
        return redirect('../')
    return HttpResponse(x)
