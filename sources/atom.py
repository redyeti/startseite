from feedbase import FeedBase

class Atom(FeedBase):
	def findDate(self, item):
		return item.find("./{http://www.w3.org/2005/Atom}updated")

	def findItems(self, doc):
		return doc.findall(".//{http://www.w3.org/2005/Atom}entry")

	def findLink(self, item):
		return item.find("./{http://www.w3.org/2005/Atom}id")

	def findTitle(self, item):
		return item.find("./{http://www.w3.org/2005/Atom}title")

if __name__ == "__main__":
	import database, config
	print list(Atom(
		name = None,
		url = "http://what-if.xkcd.com/feed.atom",
		t_keep = 0,
		t_update = 0,
	).update())
