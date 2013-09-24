from source import *
import urllib2
from lxml import etree
import re
import dateHelpers

def tt(node):
	if node is None:
		return None
	else:
		return node.text

ReType = type(re.compile(""))

class FeedBaseException(Exception):
	pass

class FeedBase(Source):
	def __init__(self, url, title=None, date=None, location=None, grep=None, delete=False, n_keep=None, user_agent=None, **params):
		Source.__init__(self, **params)
		self.__url = url
		self.__title = title
		self.__date = date
		self.__location = location
		self.__grep = grep
		self.__delete = delete
		self.__n_keep = n_keep
		self.__user_agent = user_agent

	def findDate(self, item):
		raise FeedBaseException("findDate not implemented")

	def findItems(self, doc):
		raise FeedBaseException("findItems not implemented")

	def findLink(self, item):
		raise FeedBaseException("findLink not implemented")

	def findTitle(self, item):
		raise FeedBaseException("findTitle not implemented")

	def update(self):

		print self.__url
		try:
			if self.__user_agent is None:
				req = self.__url
			else:
				req = urllib2.Request(self.__url, None, { 'User-Agent': self.__user_agent })
			u = urllib2.urlopen(req)
		except urllib2.HTTPError, e:
			print e
			return

		parser = etree.XMLParser(recover=True)
		doc = etree.XML(u.read(), parser)

		items = self.findItems(doc)
	
		n = 0

		for item in items:
			titletext = tt(self.findTitle(item))
			link = tt(self.findLink(item))
			
			if self.__title is None:
				text = titletext
			elif isinstance(self.__title, ReType):
				text = self.__title.search(titletext).groups()[0]
			else:
				text = self.__title

			if self.__date is None:
				date = dateHelpers.fuzzyParseDate(tt(self.findDate(item)))
			else:
				date = dateHelpers.fuzzyParseDate(self.__date.search(titletext).groups()[0])

			if isinstance(self.__location, ReType):
				location = self.__location.search(titletext).groups()[0]
			else:
				location = self.__location

			text = text.strip()
			location = None if location is None else location.strip()

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

