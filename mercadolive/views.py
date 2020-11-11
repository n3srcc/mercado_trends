from django.shortcuts import render
import requests as req
import json
from math import ceil
from urllib import parse
from collections import defaultdict
inbound_dict = defaultdict(list)
from .services import *

def mercado_api(url, headers={}):
    r = req.get(url, headers=headers)
    return r
    
# Create your views here.
def home(request):
    return render(request, "index.html", {})

def top_sellers(request):
    
    url = 'https://api.mercadolibre.com/sites/MLA/search?'
    res = req.get(url)
    res_dict = json.loads(res.text)

    limit = 50
    count_products = res_dict['paging']['primary_results']
    total_pages = int(ceil(count_products / limit))
    products = []

    for page in range(1, total_pages):
        res_api = mercado_api(url + parse.urlencode({'category':'MLA420040','limit':limit,'offset':page}))
        res = res_api.text
        
        res_dict = json.loads(res)
        results = res_dict.get('results')

        for product in results:
            nickname = product.get('seller').get('permalink').split("/")[-1]
            product_details = { 'id': product.get('id'), 'sold_quantity': product.get('sold_quantity'), 'seller_nickname': nickname}
            products.append(product_details)
    
    final_products = { each['seller_nickname']: each for each in products }.values()

    products = list(final_products)

    products.sort(key=lambda x: x['sold_quantity'], reverse=True)

    # for product in products[:10]:
    #     print(product)

    return render(request, "top_sellers.html", {})

def articles(request):
    res_dict = json.loads(most_expansive())
    return render(request, "articles.html", res_dict)