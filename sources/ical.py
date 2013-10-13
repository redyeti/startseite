from sources.xmlFeed import XMLFeed
from lxml import etree

class ICal(XMLFeed):

	NAMESPACES = {}

	def __init__(self, x_title=None, x_date=None, x_link=None, x_location=None, **params):
		XMLFeed.__init__(
			self,
			x_items = r".//VEVENT",
			x_title = x_title or r"string(./SUMMARY)",
			x_date = x_date or r"string(./DTSTART)",
			x_link = x_link or r"string(./URL)",
			x_location = x_location or r"string(./LOCATION)",
			**params
		)
	
	def generateDocument(self, text):
		return self.ical2xml(text)

	def ical2xml(self, text):
		doc = None
		current = None

		for line in text.split("\n"):
			tagpart, value = unicode(line, "utf8").split(":",1)
			value = value.strip().replace(r"\,",",")
			tagpart = tagpart.split(";")
			tag = tagpart[0].strip()
			print [x.split("=",1) for x in tagpart[1:]]
			attrs = dict([x.split("=",1) for x in tagpart[1:]])

			if tag == "BEGIN":
				el = etree.Element(value, **attrs)
				if doc is None:
					doc = etree.ElementTree(el)
					current = doc.getroot()
				else:
					current.append(el)
					current = el
			elif tag == "END":
				current = current.getparent()
			else:
				el = etree.Element(tag, **attrs)
				el.text = value
				current.append(el)

		return doc

if __name__ == "__main__":
	import database, config, sources
	config.Config()
	print list(ICal(
		name = None,
		url = "http://www.thetotencrackhurenimkofferraum.de/?feed=gigpress-ical",
		t_keep = 0,
		t_update = 0,
	).update())

