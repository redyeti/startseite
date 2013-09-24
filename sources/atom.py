from xmlFeed import XMLFeed

class Atom(XMLFeed):
	NAMESPACES = {
		"atom": "http://www.w3.org/2005/Atom",
	}

	def __init__(self, x_date="{}", x_items="{}", x_link="{}", x_title="{}", x_location="{}", **params):
		XMLFeed.__init__(
			self, 
			x_items = x_items.format("./atom:entry"),
			x_title = x_title.format("string(./atom:title)"),
			x_link = x_link.format("string(./atom:id)"),
			x_date = x_date.format("string(./atom:updated)"),
			x_location = x_location.format("null"),
			**params)


if __name__ == "__main__":
	import database, config, sources
	config.Config()
	print list(Atom(
		name = None,
		url = "http://what-if.xkcd.com/feed.atom",
		t_keep = 0,
		t_update = 0,
	).update())
