import requests as req

def request(params={}):
    try:
        response = req.get('https://api.mercadolibre.com/sites/MLA/search', params=params)
        if response.ok:
            return response
        else: 
            return None
            
    except request.exceptions.Timeout:
        return 'Time out, bad response'

def most_expansive():
    params = { 'category': 'MLA420040', 'sort': 'price_desc', 'limit': 10}
    return request(params)


def top_sellers():
    params = { 'category': 'MLA420040', 'sort': 'price_desc', 'limit': 10}
    return request(params)