from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def idh(request):
    return render(request,'idh.html')
