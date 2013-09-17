#!/usr/bin/env python

import time

# --- dependency injection ---
import database
import source
import config
from sources import *
from classManager import ManagedMeta, ClassManager
ClassManager.Config()

# provide plugin mechanism:
# + find modules
# - if not up to date according to db <-> INTERVAL:
#   - try to run plugin and provide item insertion interface
#   - if successful: update timestamp
#   - if not successful: log error and create an item

class Worker(object):
	__metaclass__ = ManagedMeta

	def __init__(self):
		self.db = self._CM.Database(
			self._CM.Config.DATABASE_FILE,
			self._CM.Config.prioritize
		)

	def initialize(self):
		self.db.setSources(self._CM.Source.sources.keys())
	def update(self):
		updatetime = time.time()
		for name, src in self.db.getOutOfDateSources():
			print "Updating %s ..." % name,
			counter = 0
			for item in src.update():
				if isinstance(item, source.InsertEntry):
					self.db.addItem(updatetime, name, item)
					counter += 1
				elif isinstance(item, source.CleanOldEntries):
					self.db.cleanOldEntries(name, updatetime)
				else:
					raise TypeError("Invalid item type.")

			self.db.updateSource(name, updatetime)
			self.db.commit()
			print "done. (%i Elements)" % counter

def runWorker():
	w = Worker()
	w.initialize()

	while True:
		print "Checking for updates ..."
		w.update()
		print "Up to date."
		print
		time.sleep(10)


if __name__ == "__main__":
	runWorker()
