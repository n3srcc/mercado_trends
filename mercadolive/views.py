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
            product_details = { 'id': product.get('id'), 'sold_quantity': product.get('sold_quantity'), 'nickname': nickname}
            products.append(product_details)
    
    sellers = { each['nickname']: each for each in products }.values()
    top_sellers = list(sellers)
    top_sellers.sort(key=lambda x: x['sold_quantity'], reverse=True)

    return render(request, "top_sellers.html", {'sellers': top_sellers[:10]})

def articles(request):
    try:
        res_dict = json.loads(most_expansive().text)
        return render(request, "articles.html", res_dict)
        
    except:
        raise