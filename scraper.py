from bs4 import BeautifulSoup
from datetime import datetime
from enum import Enum
import re
import requests
import time
import webbrowser
# import winsound
import cloudscraper

URLS_WORTEN = ['https://www.worten.pt/gaming/playstation/consolas/ps5/consola-ps5-825gb-7196053']
URLS_FNAC = ['https://www.fnac.pt/Bundle-PS5-Standard-Demon-s-Souls-DualSense-Consola-Consola/a9024729', 'https://www.fnac.pt/Bundle-PS5-Digital-Comando-Dual-Sense-Consola-Consola/a8492493']
URLS_MEDIAMARKT = ['https://mediamarkt.pt/products/consola-playstation-5?variant=32836255154251', 'https://mediamarkt.pt/products/conjunto-playstation-5-jogo-ps5-call-of-duty-cold-war?variant=39392380059723', 'https://mediamarkt.pt/products/conjunto-playstation-5-jogo-ps5-ratchet-clank-uma-dimensao-a-parte?variant=39392389922891', 'https://mediamarkt.pt/products/conjunto-playstation-5-jogo-ps5-call-of-duty-ratched-clank']

NOTIFY_URL = 'https://notify.run/9UBMUDRIjdbcWZQM'

ALERT_MSG = '[ALERT] {name} in stock in {store}!'

FREQUENCY_SEC = 10

COOLDOWN_DURATION_MIN = 5
ALERT_DURATION_SEC = 3

STORES = Enum('STORES', 'Worten FNAC RadioPopular MediaMarkt')

cloudscraper_instance = cloudscraper.create_scraper()

def get_products(store):
    products = None
    if store == STORES.Worten:
        products = map(cloudscraper_instance.get, URLS_WORTEN)
    elif store == STORES.FNAC:
        products = map(cloudscraper_instance.get, URLS_FNAC)
    elif store == STORES.MediaMarkt:
        products = map(requests.get, URLS_MEDIAMARKT)
    return products

def get_name(product, store):
    name = None
    if store == STORES.Worten:
        name = product.select_one('h1.w-product__name.iss-product-name').decode_contents().strip()
    elif store == STORES.FNAC:
        name = re.search('"productName"\s*:\s*"(.*?)"', str(product.find('script', id='digitalData'))).group(1)
    elif store == STORES.MediaMarkt:
        name = product.select_one('div.title > h1').decode_contents().strip()
    return name

def is_in_stock(product, store):
    result = True
    if (store == STORES.Worten and product.select_one('.w-product__actions-info__unavailable .w-product__unavailability-title').decode_contents().strip() == 'Indisponível') \
    or (store == STORES.FNAC and re.search('"availabilityID"\s*:\s*"(.*?)"', str(product.find('script', id='digitalData'))).group(1).strip() == '106') \
    or (store == STORES.MediaMarkt and product.select_one('#AddToCartText').decode_contents().strip() == 'Indisponível'):
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
            
            for product_page in get_products(store):
                product = BeautifulSoup(product_page.content, 'html.parser')
                name = get_name(product, store)
                if is_in_stock(product, store):
                    if try_open:
                        webbrowser.open(product_page.url)
                    stock = True
                print(f'{name}: {is_in_stock(product, store)}', file=log, flush=True)

            if try_open and stock:
                opened_time = time.time()
                requests.post(NOTIFY_URL, ALERT_MSG.format(name=get_name(product, store), store=store.name))
                # winsound.Beep(660, ALERT_DURATION_SEC * 1000)
                try_open = False
            elif not try_open and (time.time() - opened_time) >= (COOLDOWN_DURATION_MIN * 60):
                try_open = True
            
            if stock:
                print(ALERT_MSG.format(name=get_name(product, store), store=store.name), file=log, flush=True)
                stock = False
                
            sleep_time = next_time - time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)