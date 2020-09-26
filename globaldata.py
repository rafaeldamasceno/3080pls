from bs4 import BeautifulSoup
from datetime import datetime
import re
import requests
import time
import webbrowser
import winsound

URL_GLOBALDATA = 'https://www.globaldata.pt/componentes/placas-graficas/cat-nvidia/geforce_rtx_3080'
COOLDOWN_DURATION_MIN = 5
ALERT_DURATION_SEC = 3

next_time = time.time()
opened_time = None

opened = False
check = True

with open('globaldata.log', 'a', buffering=1) as log:

    while True:
        next_time += 10
        print(str(datetime.now()), file=log, flush=True)

        page_globaldata = requests.get(URL_GLOBALDATA)

        soup_globaldata = BeautifulSoup(page_globaldata.content, 'html.parser')

        for product in soup_globaldata.select('li.item.product'):
            name = product.select_one('div.product-item-name a strong').decode_contents()
            is_in_stock = product.select_one('div.stock-available div span').decode_contents()
            if check and is_in_stock != 'Esgotado':
                 webbrowser.open(product.select_one('div.product-item-name a')['href'])
                 opened = True
            print(f'{name}: {is_in_stock}', file=log, flush=True)

        if check and opened:
            opened_time = time.time()
            winsound.Beep(440, ALERT_DURATION_SEC * 1000)
            check = False
        elif not check and (time.time() - opened_time) >= (COOLDOWN_DURATION_MIN * 60):
            opened = False
            check = True
        
        if not check:
            print('[ALERTA] GPU em stock!', file=log, flush=True)
            
        sleep_time = next_time - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)