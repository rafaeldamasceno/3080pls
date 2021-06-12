from scraper import scraper, STORES
from threading import Thread

thread_worten = Thread(target=scraper, args=(STORES.Worten, 'log/worten.log'), daemon=False)
thread_fnac = Thread(target=scraper, args=(STORES.FNAC, 'log/fnac.log'), daemon=False)
thread_mediamarkt = Thread(target=scraper, args=(STORES.MediaMarkt, 'log/mediamarkt.log'), daemon=False)

thread_worten.start()
thread_fnac.start()
thread_mediamarkt.start()

# while input('Running. Type "q" to quit. ') != 'q':
#     pass
