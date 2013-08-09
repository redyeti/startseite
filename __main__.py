from server import runServer
from worker import runWorker
import threading 

threads = [threading.Thread(target=runServer), threading.Thread(target=runWorker)]

for t in threads:
	t.daemon = True

for t in threads:
	t.start()

for t in threads:
	try:
		t.join()
	except (KeyboardInterrupt, SystemExit):
		print "Exiting ..."
		sys.exit(1)
