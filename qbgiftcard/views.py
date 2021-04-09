from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
# Create your views here.

from qbgiftcard.models import GiftCard

from qbgiftcard.models import *

from json import dumps

from datetime import datetime, timedelta
import pytz

def qbgiftcardhome(request):
    G = GiftCard.objects.all()
    customer_dict = []
    for i in G:
        customer_dict.append([i.id, i.first_name, i.last_name, i.phone, i.email ])
    return render(request, 'qbgiftcard/default1.html', {'customer_dict': dumps(customer_dict)})


def lookup(request):
    if not request.user.is_authenticated:
        return redirect('HOME')
    try:
        x = int(request.POST['customer_id'])
        g = GiftCard.objects.get(id=x)
        staff_id = str(request.user.email).split('@fingerlakesreuse.org')[0]
        AccessLog.objects.create(staff_id=staff_id, giftcard=g)
    except:
        return HttpResponse('<h1>error occured</h1>')
    return redirect('qbgiftcard:results')




def results(request):
    if not request.user.is_authenticated:
        return redirect('HOME')
    try:
        staff_id = str(request.user.email).split('@fingerlakesreuse.org')[0]
        last_record = AccessLog.objects.filter(staff_id=staff_id).reverse().order_by('timestamp')[0]
        gift_card_code = GiftCard.objects.get(id=last_record.giftcard_id).giftcard
        gift_card_code = gift_card_code.replace(' ','')

    except:
        return redirect('qbgiftcard:qbgiftcardhome')
    return render(request, 'qbgiftcard/lookup1.html', {'gift_card_code': gift_card_code})




def giftcard(request):
    return HttpResponse('working - giftcard')

def log(request):
    return HttpResponse('working - log')



def tester1(request, a=10):
    return HttpResponse(a)

def tester2(request):
    return redirect('qbgiftcard:tester1', a=20)
