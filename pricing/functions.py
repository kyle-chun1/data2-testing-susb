from .models import *
from time import sleep
from local_settings import *
import json
import requests

#Reportlab - Barcodes
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import qr
from reportlab.lib.units import inch
import io



def fill_variants_color(handle):
    #Step 1: Try and get the handle and report the Response code
    print(S_URL)
    request = requests.get(S_URL + 'products.json', params={'handle':handle})
    print(f'Request Status Code of "{handle}": {request.status_code}')
    response = json.loads(request.text)
    #Step 2: Print out a list of titles that it received
    #Step 3: Add each of them to the database
    try:
        product = response['products'][0]
        Q = Product.objects.get(shopify_handle = handle.upper().strip())
        print(Q, 'now going to add them to the database')
        sleep(4)
        for i in product['variants']:
            print(f'{i["id"]}  {i["title"]}', end='\t')
            try:
                QQ = Variant(product=Q, title=i['title'], price=float(i['price']), variant=i['sku']).save()

            except:
                print('ERROR OCCURER ^ - moving to next')

    except:
        print('FAILED - no product found / Error occured')

    print('\n DONE')
    pass





def fill_variants_unit(handle):
    #Step 1: Try and get the handle and report the Response code
    print(S_URL)
    request = requests.get(S_URL + 'products.json', params={'handle':handle})
    print(f'Request Status Code of "{handle}": {request.status_code}')
    response = json.loads(request.text)
    #Step 2: Print out a list of titles that it received
    #Step 3: Add each of them to the database
    try:
        product = response['products'][0]
        Q = Product.objects.get(shopify_handle = handle.upper().strip())
        print(Q, 'now going to add them to the database')
        sleep(4)
        for i in product['variants']:
            print(f'{i["id"]}  {i["title"]}', end='\t')
            try:
                QQ = Variant(product=Q, title=i['title'], price=float(i['price']), variant=i['sku']).save()

            except:
                print('ERROR OCCURER ^ - moving to next')

    except:
        print('FAILED - no product found / Error occured')

    print('\n DONE')
    pass





def barcode_reuse_1(VARIANT,PRICE,TITLE, COLOR, HANDLE, QUANTITY):
    TITLE = TITLE.split(' -[')[0]
    X = 1.25 * inch
    Y = 0.85 * inch
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=(X,Y))
    c.setTitle('BARCODE - Finger Lakes ReUse Inc.')
    #PRICE
    PRICE = f'${PRICE:.2f}'
    for i in range(QUANTITY):
        c.setFont("Helvetica-Bold", 16,)
        c.drawString(X*0.05,Y*0.72,f'{PRICE:>10}')
        #LINE
        c.line(X*0.2,Y*0.635,X*0.8,Y*0.635)
        #QR
        qr_code = qr.QrCode(VARIANT, height=X*0.43,width=X*0.43)
        qr_code.drawOn(c,X*0.0,Y*0.0)
        #TITLE
        if len(TITLE)<14:
            c.setFont("Helvetica-Bold", 8)
        else:
            c.setFont("Helvetica-Bold", 6)
        c.drawString(X*0.41, Y*0.45,f'{TITLE}')
        #COLOR
        c.setFont("Helvetica-Bold", 6)
        c.drawString(X*0.41,Y*0.275,f'{COLOR}')
        #HANDLE
        c.setFont("Helvetica", 6)
        c.drawString(X*0.41,Y*0.10,f'{HANDLE}')
        c.showPage()

    c.save()
    buffer.seek(0)
    return buffer
