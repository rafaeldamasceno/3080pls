from scraper import scraper, STORES
from threading import Thread

thread_worten = Thread(target=scraper, args=(STORES.Worten, 'worten.log'), daemon=True)
thread_fnac = Thread(target=scraper, args=(STORES.FNAC, 'fnac.log'), daemon=True)
thread_mediamarkt = Thread(target=scraper, args=(STORES.MediaMarkt, 'mediamarkt.log'), daemon=True)

thread_worten.start()
thread_fnac.start()
thread_mediamarkt.start()

while input('Running. Type "q" to quit. ') != 'q':
    pass
