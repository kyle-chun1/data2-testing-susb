from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.timezone import datetime
from .models import RawMaterialMovement, ExpandedMaterialMovement
import requests
import json
from .functions import ExpansionFunction


# 2021 Extention
from mm.models import Pallet,Movement
from pricing.models import ProductType
from visitors.functions import start_end_date

from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum

def mm(request):
    return redirect('mm:movement')
    #IF USER IS NOT AUTHENTICATED SEND THEM HOME!
    if not request.user.is_authenticated:
        return redirect('HOME')

    return_dict = {
        'tDate' : str(datetime.today())[0:10],          #################NEED TO FIGURE OUT THE TIMEZONE DIFF!!!
        'tTimestamp' : str(datetime.now().timestamp()),
        'tName' : request.user.email,
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



from .models import ExpandedMaterialMovement

def rawdata(request):
    E = ExpandedMaterialMovement.objects.all()
    print('\n\n\n\n',dict(vars(E[0])).keys(),'\n\n\n\n')
    for i in E:
        temp = dict(vars(i))
        for j in temp:
            print(temp[j], end=',')
        print()
    return HttpResponse('WORKING')






################################################################
# 2021 REDO OF MATERIAL Movement
################################################################


def movement(request):
    #IF USER IS NOT AUTHENTICATED SEND THEM HOME!
    if not request.user.is_authenticated:
        return redirect('HOME')

    # RECORDS = Movement.objects.filter(staff_id = str(request.user.email).split('@')[0])\
        # .order_by('-timestamp')[0:20]
    RECORDS = Pallet.objects.filter(\
        movement__staff_id = str(request.user.email).split('@')[0],
        movement__timestamp__range=( timezone.now()-timedelta(days=7) ,  timezone.now()  )   )\
        .values('id','movement__timestamp','movement__origin_type','movement__origin_location','movement__destination_type','movement__destination_location','product_type__product_type','quantity')

    return_dict = {
        'product_type_list' : [[i.product_type,i.id] for i in ProductType.objects.all().order_by('product_type')],
        'header_subtitle': '',
        'RECORDS' : RECORDS,

    }
    # IF THERE WAS A RECENT TRANSACTION, THEN PLEASE ADD IN A RECORD FOR THAT

    return render(request,'mm/movement.html', return_dict)




####################################
# MOVEMENT SUBMISSION Form
####################################

def movement_submit(request):
    origin_location = request.POST.get('origin_location')
    origin_type = request.POST.get('origin_type')
    destination_location = request.POST.get('destination_location')
    destination_type = request.POST.get('destination_type')
    material_list = request.POST.get('pallets')
    pallets_raw = json.loads(material_list)

    # FLATTEN LIST
    pallets = dict()
    for i in pallets_raw:
        if i[0] in pallets:
            pallets[i[0]] += float(i[1])
        else:
            pallets[i[0]] = float(i[1])

    staff_id = str(request.user.email).split('@fingerlakesreuse.org')[0]

    # FIRST SUBMIT TO MOVEMENT # DB
    movement_id = Movement.objects.create(
        origin_type=origin_type, origin_location=origin_location, destination_type=destination_type, destination_location=destination_location, staff_id=staff_id
    )

    # SUBMIT THE FLATTEN LIST ONE BY ONE TO THE # DB:
    pallet_db = Pallet.objects
    for i in pallets:
        pallet_db.create(movement=movement_id, product_type=ProductType.objects.get(id=int(i))   ,quantity=pallets[i])

    # return HttpResponse( f'{origin_type}, {origin_location}, {destination_type}, {destination_location}, {pallets}')
    return redirect('mm:movement')




####################################
# STATS - INITIAL
####################################
def stats(request):
    #IF USER IS NOT AUTHENTICATED SEND THEM HOME!
    if not request.user.is_authenticated:
        return redirect('HOME')

    start_date, end_date = start_end_date(request.GET)

    return_dict = {
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
    }
    return render(request, 'mm/stats.html', return_dict)



def raw(request):
    #IF USER IS NOT AUTHENTICATED SEND THEM HOME!
    if not request.user.is_authenticated:
        return redirect('HOME')

    start_date, end_date = start_end_date(request.GET)

    RECORDS = Pallet.objects.filter(\
        movement__staff_id = str(request.user.email).split('@')[0],
        movement__timestamp__range=( timezone.now()-timedelta(days=7) ,  timezone.now()  )   )\
        .values('movement__staff_id','movement__timestamp','movement__origin_type','movement__origin_location','movement__destination_type','movement__destination_location','product_type__product_type','quantity')


    return_dict = {
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'RECORDS' : RECORDS,
    }

    return render(request,'mm/raw.html', return_dict)
