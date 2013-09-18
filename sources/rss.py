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

class RSS(Source):
	def __init__(self, url, title=None, date=None, location=None, grep=None, delete=False, n_keep=None, **params):
		Source.__init__(self, **params)
		self.__url = url
		self.__title = title
		self.__date = date
		self.__location = location
		self.__grep = grep
		self.__delete = delete
		self.__n_keep = n_keep

	def update(self):

		u = urllib2.urlopen(self.__url)
		doc = etree.XML(u.read())

		items = doc.findall(".//item")
	
		n = 0

		for item in items:
			titletext = tt(item.find("./title"))
			link = tt(item.find("./link"))
			
			if self.__title is None:
				text = titletext
			elif isinstance(self.__title, ReType):
				text = self.__title.search(titletext).groups()[0]
			else:
				text = self.__title

			if self.__date is None:
				date = dateHelpers.fuzzyParseDate(tt(item.find("./pubDate")))
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

if __name__ == "__main__":
	import database, config
	print list(RSS(
		name = None,
		url = "http://hannover.prinz.de/termine/veranstaltungen?search=&primetime=&location_id=&sort=date&main_cat_id=1&hide_form=0&cat_id[0]=1&cat_id[1]=100&cat_id[2]=1214065&cat_id[3]=1214067&cat_id[4]=1214069&cat_id[5]=1291239&date_from=17.09.2013&date_to=31.12.2013&feed=rss",
		title = re.compile(r"^(.*\))"),
		date = re.compile(r"- (.*)$"),
		location = re.compile(r"\)(.*)-"),
		t_keep = 0,
		t_update = 0,
	).update())
