from bs4 import BeautifulSoup
from datetime import datetime
import re
import requests
import time
import webbrowser
import winsound

URL_PCDIGA = 'https://www.pcdiga.com/catalogo-pcdiga/componentes/placas-graficas/graficas-nvidia/pg_grafica_filtro-geforce_rtx_3080?product_list_order=price'
COOLDOWN_DURATION_MIN = 5
ALERT_DURATION_SEC = 3

next_time = time.time()
opened_time = None

opened = False
check = True

with open('pcdiga.log', 'a', buffering=1) as log:

    while True:
        next_time += 10
        print(str(datetime.now()), file=log, flush=True)

        page_pcdiga = requests.get(URL_PCDIGA)

        soup_pcdiga = BeautifulSoup(page_pcdiga.content, 'html.parser')

        for product in soup_pcdiga.find_all(class_='product-card'):
            name = product.find('div', class_='product-card--title')['title']
            script = product.find('script')
            is_in_stock = re.search("'is_in_stock'.*?:.*?(\d+).*?,", str(script)).group(1)
            if check and is_in_stock != '0':
                webbrowser.open(product.find('a')['href'])
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