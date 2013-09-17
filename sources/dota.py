from source import *
import urllib2
from lxml import etree

class Dota(Source):
	def update(self):

		url = "http://www.kleingeldprinzessin.de"
		u = urllib2.urlopen(url)
		doc = etree.HTML(u.read())

		tour = doc.xpath(".//h2[./text()='Tourdaten']")[0]
		dateElements = tour.getparent().findall("h4")
	
		for dateElement in dateElements:
			date = dateElement.text
			text = etree.tostring(dateElement.getnext(), method="text", encoding=unicode)
			textparts = text.split(",")
			if len(textparts) <= 1:
				continue
			date = parseDate(date, ["%d.%m.%Y", "%d.%m.%Y um %H:%M h"])
			location = textparts[0].capitalize().strip()
			text = "Dota in %s (%s)" % (location, textparts[1].strip())
			yield InsertEntry(date, text, location, url)

		yield CleanOldEntries()

if __name__ == "__main__":
	import database, config
	print list(Dota(None, 0, 0).update())
