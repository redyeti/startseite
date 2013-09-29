#!/usr/bin/env python

import time, sys
import urllib2
import traceback

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

	@property
	def db(self):
		return self._CM.Config.db

	def __init__(self, nofail=True):
		self.db.setSources(self._CM.Source.sources.keys())
		self.__nofail = nofail

	def update(self):
		updatetime = time.time()
		for name, src in self.db.getOutOfDateSources():
			self.__updateOne(name, src, updatetime)
		registry = self.db.getGlobalView()
		registry["workerTimestamp"] = updatetime

	def __updateOne(self, name, src, updatetime):
		print "Updating %s ..." % name,
		sys.stdout.flush()
		counter = 0

		try:
			for item in src.update():
				if isinstance(item, source.InsertEntry):
					self.db.addItem(updatetime, name, item)
					counter += 1
				elif isinstance(item, source.CleanOldEntries):
					self.db.cleanOldEntries(name, updatetime)
				else:
					raise TypeError("Invalid item type: %s" % type(item))
			self.db.updateSource(name, updatetime)
			self.db.commit()
			print "done. (%i Elements)" % counter
		except: #sic!
			if self.__nofail:
				traceback.print_exc()
				self.db.rollback()
			else:
				raise

	def runOnce(self):
		print "Checking for updates ..."
		self.update()
		print "Up to date."

	def run(self):
		while True:
			self.runOnce()
			print
			time.sleep(10)
		

if __name__ == "__main__":
	Worker().run()

