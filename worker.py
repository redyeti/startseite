#!/usr/bin/env python

import time
import config
from database import Database

# provide plugin mechanism:
# + find modules
# - if not up to date according to db <-> INTERVAL:
#   - try to run plugin and provide item insertion interface
#   - if successful: update timestamp
#   - if not successful: log error and create an item

class Worker(object):
	def __init__(self):
		self.db = Database(config.DATABASE)

	def initialize(self):
		self.db.setSources(config.SOURCES)
	def update(self):
		updatetime = time.time()
		for name, source in self.db.getOutOfDateSources():
			print "Updating",name
			for item in source.update(name):
				self.db.addItem(updatetime, name, item)
			self.db.updateSource(name, updatetime)

def runWorker():
	w = Worker()
	w.initialize()

	while True:
		print "Worker ..."
		w.update()
		time.sleep(10)


if __name__ == "__main__":
	runWorker()
