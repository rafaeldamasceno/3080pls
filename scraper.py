from bs4 import BeautifulSoup
from datetime import datetime
from enum import Enum
import re
import requests
import time
import webbrowser
import winsound

NOTIFY_URL = 'https://notify.run/zRunWfXWbBRYwROz'
ALERT_MSG = '[ALERT] GPU in stock!'
COOLDOWN_DURATION_MIN = 5
ALERT_DURATION_SEC = 3

STORES = Enum('STORES', 'PCDIGA Globaldata')

def get_products(soup, store):
    products = None
    if store == STORES.PCDIGA:
        products = soup.find_all(class_='product-card')
    elif store == STORES.Globaldata:
        products = soup.select('li.item.product')
    return products

def get_name(product, store):
    name = None
    if store == STORES.PCDIGA:
        name = product.find('div', class_='product-card--title')['title']
    elif store == STORES.Globaldata:
        name = product.select_one('div.product-item-name a strong').decode_contents()
    return name

def get_product_link(product, store):
    link = None
    if store == STORES.PCDIGA:
        link = product.find('a')['href']
    elif store == STORES.Globaldata:
        link = product.select_one('div.product-item-name a')['href']
    return link

def is_in_stock(product, store):
    result = False
    if store == STORES.PCDIGA and re.search("'is_in_stock'.*?:.*?(\d+).*?,", str(product.find('script'))).group(1) != '0':
        result = True
    elif store == STORES.Globaldata and product.select_one('div.stock-available div span').decode_contents() != 'Esgotado':
        result = True
    return result

def scraper(url, log_name, store):
    next_time = time.time()
    opened_time = None

    try_open = True
    stock = False

    with open(log_name, 'a', buffering=1) as log:

        while True:
            next_time += 10
            print(str(datetime.now()), file=log, flush=True)

            page = requests.get(url)

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
                winsound.Beep(660, ALERT_DURATION_SEC * 1000)
                requests.post(NOTIFY_URL, ALERT_MSG)
                try_open = False
            elif not try_open and (time.time() - opened_time) >= (COOLDOWN_DURATION_MIN * 60):
                try_open = True
            
            if stock:
                print(ALERT_MSG, file=log, flush=True)
                stock = False
                
            sleep_time = next_time - time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)