from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def tester2(request):
    return render(request,'pricing/pricing_trc.html', {})
