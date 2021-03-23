from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, FileResponse


from pricing.functions import barcode_reuse_1


# Create your views here.
def tester2(request, x=1):
    for i in range(20): print(request.session.get('msg','DEFAULT'))
    request.session['msg'] = None
    return render(request,'pricing/pricing_trmc.html', {})


##########
def tester3(request):
    Y = barcode_reuse_1('WTBMM1500',1500,'Building Materials', 'WHITE', 'WTBMM', 2)
    request.session['message'] = 'success'
    return FileResponse(Y, as_attachment=False, filename="barcode.pdf")

def tester_main(request, yolo=1):
    if 1==1:
        request.session['msg'] = 'GOOOOOOGLE'
        return redirect(reverse('pricing:tester2'))
    return render(request, 'pricing/tester_main.html', {})

def tester_submit(request):
    HttpResponse('SUBMITTED')
##########




def pricing_portal(request, location):
    # LOCATION SLUG CHECK
    if location.upper() in ['TRMC', 'TRC', 'TRMC']:
        location = 'trmc'
    else:
        return(redirect('/'))

    #MESSAGE CHECK
    if 'message' in request.session and request.session['message'] == 'success':
        message = 'SUCCESS'
        request.session['message'] = ''
    else:
        request.session['message'] = ''
        message=''

    print(request.user.email)

    return render(request, 'pricing/pricing_trmc.html',{'message': message})





def pricing_submit(request, location):
    # LOCATION SLUG CHECK
    if location.upper() in ['TMRC', 'TRC', 'TRMC']:
        location = 'trmc'
    else:
        return(redirect('/'))

    #ANALYZE THE QUANTITY


    #ANALYZE THE POST VARIABLES



    request.session['messsage'] = 'success'
    return redirect(reverse('pricing:portal', kwargs={'location': location}))
