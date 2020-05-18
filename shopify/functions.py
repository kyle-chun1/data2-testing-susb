from local_settings import S_URL

import requests
from bs4 import BeautifulSoup
import json
import re



#######################################################################################################
#SURE FUNCTION - Definitely returns something
#Function will raise an error for invalid code or inability to get sucessful parameters
def acetap_function(code):
    request = requests.get(f'https://www.acehardware.com/search?searchSettings=lowerMatch&query={code}')
    request.encoding = 'utf-8'
    if request.status_code!=200  or  request.url.strip()[:40]!='https://www.acehardware.com/departments/':
        raise NameError
    else:
        data = json.loads(re.findall(r'<script type="text/json" id="data-mz-preload-product">(.*?)</script>',request.text)[0])
        soup = BeautifulSoup(request.text,'html.parser')

        #COMPLIE THE SALE AND REGULAR PRICE
        if data['price']['onSale'] == True:
            saleprice = data['price']['salePrice']
        else:
            saleprice = data['price']['price']

        #COMPILE THE SPECS, FEATURES, ETC.
        features = []
        specifications = {}
        producttype = ''
        whatsinthebox = ''
        try:
            for i in data['properties']:
                if not i['isHidden']:
                    if 'stringValue' in i['values'][0]:
                        if 'tenant~feature-' in i['attributeFQN']:
                            features.append(i['values'][0]['stringValue'])
                        if 'tenant~whats-in-the-box' in i['attributeFQN']:
                            whatsinthebox = i['values'][0]['stringValue']
                        if 'tenant~A0' in i['attributeFQN']:
                            specifications[i['attributeDetail']['name']] = i['values'][0]['stringValue']
                        if 'tenant~product-type' in i['attributeFQN']:
                            producttype = i['values'][0]['stringValue']
        except:
            pass


        return {
            'url': request.url,
            'code' : code,
            'title': data['content']['productName'].strip(),
            'mpn': data['mfgPartNumber'].strip(),
            'description' : data['content']['productFullDescription'].strip(),
            'category1': request.url[40:].split('/')[0],
            'category2': request.url[40:].split('/')[1],
            'category3': request.url[40:].split('/')[2],
            'photos':  ['https:' + i['src'] for i in data['content']['productImages']],

            'price': data['price']['price'],
            'saleprice': saleprice,

            'producttype': producttype,
            'whatsinthebox' : whatsinthebox,
            'features': features,
            'specifications': specifications,

        }


#######################################################################################################
# TESTER FUNCTION - THIS IS USE FOR PRE-TESTING and DEPLOYMENT OF A FUNCTION
# UNSURE FUNCTION  - ERROR AT ANY FAIL
# MULTIPLE REQUETST!!!!
def test_function(endpoint_url='',params={}, endpoint=''):
    the_request_url = S_URL + endpoint_url
    the_request = requests.get(the_request_url,params=params)
    return_list = json.loads(the_request.text)[endpoint]

    while('next' in the_request.links):
        the_request_url = the_request.links['next']['url']
        the_request_url = the_request_url.replace('https://fingerlakesreuse.myshopify.com/admin/api/2020-04/',S_URL)
        print('\n\nBEFORE',the_request.links,'\n')
        the_request = requests.get(the_request_url)
        print('\n\nAFTER',the_request.links,'\n\n\n')
        return_list += json.loads(the_request.text)[endpoint]


    # if 'Link' in the_request.headers:
    #     print('\n\n',the_request.links,'\n\n')
    return return_list


#######################################################################

def FINAL_import():
    import pandas as pd
    from shopify.models import AceInventoryList
    FINAL = pd.read_csv('FINAL.csv')
#    AceInventory.objects.all().delete()
    for i in range(FINAL.shape[0]):
        FINAL_dict = {
            'Index' : i,
            'ItemCode' : FINAL.loc[i]['SKU'],
            'Location' : FINAL.loc[i]['Loc'],
            'Department' : FINAL.loc[i]['Dept #'],
            'Title' : FINAL.loc[i]['Description'],
            'Upc' : FINAL.loc[i]['UPC'],
            'Qoh' : FINAL.loc[i]['QOH'],
            'Mpn' : FINAL.loc[i]['Mfg Part #'],
            'Retail' : FINAL.loc[i]['Retail'],
            'Status' : FINAL.loc[i]['STATUS'],
        }
        AceInventoryList.objects.create(**FINAL_dict).save()
        print(FINAL_dict)
