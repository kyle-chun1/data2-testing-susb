from django.shortcuts import render
from django.http import HttpResponse

from mm.models import ExpandedMaterialMovement as e
from django.db.models import Sum

# Create your views here.
def materialflow(request):



    return render(request,'materialflow.html', {
    'total_pallets' : int(e.objects.filter(eOrigin='donations').aggregate(Sum('ePallets'))['ePallets__sum']),
    'total_to_processing' : int(e.objects.filter(eOrigin='donations',eDestination='processing').aggregate(Sum('ePallets'))['ePallets__sum']),
    'total_to_overflow' : int(e.objects.filter(eOrigin='donations', eDestination='overflow').aggregate(Sum('ePallets'))['ePallets__sum']),

    'processing_from_ddo' : int(e.objects.filter(eOrigin='donations', eDestination='processing').aggregate(Sum('ePallets'))['ePallets__sum']),
    'processing_from_overflow' : int(e.objects.filter(eOrigin='overflow', eDestination='processing').aggregate(Sum('ePallets'))['ePallets__sum']),
    'processing_to_irc' : int(e.objects.filter(eDestination='processing',eDestinationLocation='IRC').aggregate(Sum('ePallets'))['ePallets__sum']),
    'processing_to_trc' : int(e.objects.filter(eDestination='processing',eDestinationLocation='TRC').aggregate(Sum('ePallets'))['ePallets__sum']),
    })
