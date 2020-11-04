from bs4 import BeautifulSoup
from datetime import datetime
from enum import Enum
import re
import requests
import time
import webbrowser
import winsound

URL_PCDIGA = 'https://www.pcdiga.com/catalogo-pcdiga/componentes/processadores/processadores-amd/cpu_arquitetura-zen_3'
URL_GLOBALDATA = 'https://www.globaldata.pt/componentes/processadores/amd-zen_3'
URL_NOVOATALHO = 'https://www.novoatalho.pt/actions/products/GetProducts.ashx'

NOTIFY_URL = 'https://notify.run/CtjOqFQNWmukdVWF'

ALERT_MSG = f'[ALERT] CPU in stock!'

FREQUENCY_SEC = 10

COOLDOWN_DURATION_MIN = 5
ALERT_DURATION_SEC = 3

STORES = Enum('STORES', 'PCDIGA Globaldata NovoAtalho')

def get_page(store):
    page = None
    if store == STORES.PCDIGA:
        page = requests.get(URL_PCDIGA)
    elif store == STORES.Globaldata:
        page = requests.get(URL_GLOBALDATA)
    elif store == STORES.NovoAtalho:
        page = requests.post(URL_NOVOATALHO, json={"id":11209,"countpage":1,"brands":[],"min":-1,"max":-1,"stockFilters":[],"attributeFilters":[{"name":"Arquitetura do CPU","group":"","value":"Zen 3"}],"type":"grid","sortby":0,"itensList":20,"reset":True,"categories":[],"campaigns":[],"isoutlet":[],"ishighlight":[],"ispresale":[],"hasoffer":[]})
    return page


def get_products(soup, store):
    products = None
    if store == STORES.PCDIGA:
        products = soup.find_all(class_='product-card')
    elif store == STORES.Globaldata:
        products = soup.select('li.item.product')
    elif store == STORES.NovoAtalho:
        products = soup.find_all('div', class_='product')
    return products

def get_name(product, store):
    name = None
    if store == STORES.PCDIGA:
        name = product.find('div', class_='product-card--title')['title']
    elif store == STORES.Globaldata:
        name = product.select_one('div.product-item-name a strong').decode_contents()
    elif store == STORES.NovoAtalho:
        name = product.select_one('h2 a')['title']
    return name

def get_product_link(product, store):
    link = None
    if store == STORES.PCDIGA:
        link = product.find('a')['href']
    elif store == STORES.Globaldata:
        link = product.select_one('div.product-item-name a')['href']
    elif store == STORES.NovoAtalho:
        link = product.select_one('h2 a')['href']
    return link

def is_in_stock(product, store):
    result = True
    if (store == STORES.PCDIGA and re.search("'is_in_stock'.*?:.*?(\d+).*?,", str(product.find('script'))).group(1) == '0') \
    or (store == STORES.Globaldata and product.select_one('div.stock-available div span').decode_contents().strip() == 'Esgotado') \
    or (store == STORES.NovoAtalho and product.select_one('span.stock b a').decode_contents().strip() == 'Indisponível'):
        result = False
    return result

def scraper(store, log_name):
    next_time = time.time()
    opened_time = None

    try_open = True
    stock = False

    with open(log_name, 'a', buffering=1) as log:

        while True:
            next_time += FREQUENCY_SEC
            print(str(datetime.now()), file=log, flush=True)

            page = get_page(store)

            soup = BeautifulSoup(page.content, 'html.parser')
            
            for product in get_products(soup, store):
                name = get_name(product, store)
                if is_in_stock(product, store):
                    if try_open:
                        webbrowser.open(get_product_link(product, store))
                    stock = True
                print(f'{name}: {is_in_stock(product, store)}', file=log, flush=True)

            if try_open and stock:
                opened_time = time.time()
                requests.post(NOTIFY_URL, ALERT_MSG)
                winsound.Beep(660, ALERT_DURATION_SEC * 1000)
                try_open = False
            elif not try_open and (time.time() - opened_time) >= (COOLDOWN_DURATION_MIN * 60):
                try_open = True
            
            if stock:
                print(ALERT_MSG, file=log, flush=True)
                stock = False
                
            sleep_time = next_time - time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)