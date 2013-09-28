from ..feedbase import FeedBase
from lxml import etree
from abc import abstractproperty
from xfnExtensions import xfn

class XMLFeed(FeedBase):
	PARSER = etree.XMLParser
	DOCUMENT = etree.XML

	NAMESPACES = abstractproperty()

	def __init__(self, x_items, x_title, x_link, x_date, x_location, **params):
		FeedBase.__init__(self, **params)
		self.__xItems = x_items
		self.__xTitle = x_title
		self.__xLink = x_link
		self.__xDate = x_date
		self.__xLocation = x_location

	def __check(self, t):
		if t == []:
			return None
		elif isinstance(t, list):
			return t[0]
		return t
	
	def findItems(self, doc):
		return doc.xpath(self.__xItems, namespaces = self.NAMESPACES)

	def findTitle(self, item):
		print self.__xTitle
		ret = item.xpath(self.__xTitle, namespaces = self.NAMESPACES)
		return self.__check(ret)

	def findDate(self, item):
		ret = item.xpath(self.__xDate, namespaces = self.NAMESPACES)
		print "DATE:", ret
		return self.__check(ret)

	def findLink(self, item):
		ret = item.xpath(self.__xLink, namespaces = self.NAMESPACES)
		print "LINK:", ret
		return self.__check(ret)

	def findLocation(self, item):
		ret = item.xpath(self.__xLocation, namespaces = self.NAMESPACES)
		return self.__check(ret)

	def generateDocument(self, text):
		parser = self.PARSER(recover=True)
		return self.DOCUMENT(text, parser)

class HTMLFeed(XMLFeed):
	PARSER = etree.HTMLParser
	DOCUMENT = etree.HTML
	NAMESPACES = {}
