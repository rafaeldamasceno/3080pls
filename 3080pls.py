from scraper import scraper, STORES
from threading import Thread

thread_pcdiga = Thread(target=scraper, args=(STORES.PCDIGA, 'pcdiga.log'), daemon=True)
thread_globaldata = Thread(target=scraper, args=(STORES.Globaldata, 'globaldata.log'), daemon=True)
thread_novoatalho = Thread(target=scraper, args=(STORES.NovoAtalho, 'novoatalho.log'), daemon=True)

thread_pcdiga.start()
thread_globaldata.start()
thread_novoatalho.start()

while input('Running. Type "q" to quit. ') != 'q':
    pass