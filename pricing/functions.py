from .models import *
from time import sleep
from local_settings import *
import json
import requests

def fill_variants(handle):
    #Step 1: Try and get the handle and report the Response code
    print(S_URL)
    request = requests.get(S_URL + 'products.json', params={'handle':handle})
    print(f'Request Status Code of "{handle}": {request.status_code}')
    response = json.loads(request.text)
    #Step 2: Print out a list of titles that it received
    #Step 3: Add each of them to the database
    try:
        product = response['products'][0]
        for i in product['variants']: print(f'{i["id"]}  {i["title"]}')
    except:
        print('FAILED - no product found')
    pass
