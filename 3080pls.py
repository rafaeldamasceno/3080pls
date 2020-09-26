from scraper import scraper, STORES
from threading import Thread

URL_PCDIGA = 'https://www.pcdiga.com/catalogo-pcdiga/componentes/placas-graficas/graficas-nvidia/pg_grafica_filtro-geforce_rtx_3080?product_list_order=price'
URL_GLOBALDATA = 'https://www.globaldata.pt/componentes/placas-graficas/cat-nvidia/geforce_rtx_3080'

thread_pcdiga = Thread(target=scraper, args=(URL_PCDIGA, 'pcdiga.log', STORES.PCDIGA), daemon=True)
thread_globaldata = Thread(target=scraper, args=(URL_GLOBALDATA, 'globaldata.log', STORES.Globaldata), daemon=True)

thread_pcdiga.start()
thread_globaldata.start()

while input('Running. Type "q" to quit. ') != 'q':
    pass