#-*- coding: utf8 -*-
from __future__ import unicode_literals
from source import *
import urllib2
import time

class Diff(Source):
	def __init__(self, url, **params):
		Source.__init__(self, **params)
		self.__url = url
	def update(self):
		dhash = hash(self.fetch())
		
		if "hash" not in self.registry or self.registry["hash"] != dhash:
			self.registry["hash"] = dhash
			yield InsertEntry(time.time(), "Seite \"%s\" Geändert" % self.name, None, self.__url)	
			

	def fetch(self):
		u = urllib2.urlopen(self.__url)
		return u.read()
		
