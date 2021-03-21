from .models import *
from time import sleep
from local_settings import *
import json
import requests

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
    pass
