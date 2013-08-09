from source import *
import urllib2

class Dota(Source):
	def update(self, name):
		u = urllib2.urlopen("http://www.kleingeldprinzessin.de/dota/pages_de_de/startseite/startseite/events.txt")
		lines = iter([x.strip() for x in u.read().split("\n")])
		
		assert(lines.next() == "eventstext=")
		try:
			while True:
				date = lines.next()

				if not date:
					continue

				date = parseDate(date, ["%d.%m.%Y", "%d.%m.%Y um %H:%M h"])
				text = lines.next()
				
				t = text.replace(">","|").replace("<","|").split("|")
				itemtext = "Dota " + t[0][:-4]
				location = t[2]

				yield InsertEntry(date, itemtext, location, None)
				if lines.next() != "":
					raise ValueError("Expected empty line.")

		except StopIteration:
			return
