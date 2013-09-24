from source import *
import urllib2
import dateHelpers

from classManager import ManagedABCMeta
from abc import abstractmethod

class FeedBase(Source):
	__metaclass__ = ManagedABCMeta

	def __init__(self, url, title=None, date=None, location=None, grep=None, delete=False, n_keep=None, user_agent=None, **params):
		Source.__init__(self, **params)
		self.__url = url
		self.__grep = grep
		self.__delete = delete
		self.__n_keep = n_keep
		self.__user_agent = user_agent

	@abstractmethod
	def findDate(self, item):
		pass

	@abstractmethod
	def findItems(self, doc):
		pass

	@abstractmethod
	def findLink(self, item):
		pass

	@abstractmethod
	def findTitle(self, item):
		pass

	@abstractmethod
	def findLocation(self, item):
		pass

	@abstractmethod
	def generateDocument(self, text):
		pass

	def update(self):
		try:
			if self.__user_agent is None:
				req = self.__url
			else:
				req = urllib2.Request(self.__url, None, { 'User-Agent': self.__user_agent })
			u = urllib2.urlopen(req)
		except urllib2.HTTPError, e:
			print e
			return

		doc = self.generateDocument(u.read())

		items = self.findItems(doc)
	
		n = 0

		for item in items:
			
			text = self.findTitle(item)
			date = dateHelpers.fuzzyParseDate(self.findDate(item))
			location = self.findLocation(item)
			link = self.findLink(item)

			text = text.strip()
			location = None if location is None else location.strip()
			lnk = None if link is None else link.strip()

			if (
				self.__grep is None or
				(isinstance(self.__grep, basestring) and self.__grep in text) or
				(isinstance(self.__grep, ReType) and self.__grep.search(text))):

				yield InsertEntry(date, text, location, link)
				n += 1

			if self.__n_keep is not None and n >= self.__n_keep:
				break

		if self.__delete:
			yield CleanOldEntries()

