from bs4 import BeautifulSoup
from datetime import datetime
import re
import requests
import time
import webbrowser
import winsound

URL_GLOBALDATA = 'https://www.globaldata.pt/componentes/placas-graficas/cat-nvidia/geforce_rtx_3080'

next_time = time.time()

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
            winsound.Beep(440, 2000)
            check = False
            
        sleep_time = next_time - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)