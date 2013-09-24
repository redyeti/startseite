from xmlFeed import XMLFeed

class RSS(XMLFeed):
	NAMESPACES = {}

	def __init__(self, x_date="{}", x_items="{}", x_link="{}", x_title="{}", x_location="{}", **params):
		XMLFeed.__init__(
			self, 
			x_items = x_items.format(".//item"),
			x_title = x_title.format("string(./title)"),
			x_link = x_link.format("string(./link)"),
			x_date = x_date.format("string(./pubDate)"),
			x_location = x_location.format("xfn:null()"),
			**params)

if __name__ == "__main__":
	import database, config, sources
	config.Config()
	print list(RSS(
		name = None,
		url = "http://hannover.prinz.de/termine/veranstaltungen?search=&primetime=&location_id=&sort=date&main_cat_id=1&hide_form=0&cat_id[0]=1&cat_id[1]=100&cat_id[2]=1214065&cat_id[3]=1214067&cat_id[4]=1214069&cat_id[5]=1291239&date_from=17.09.2013&date_to=31.12.2013&feed=rss",
		x_title = r"xfn:search('^(.*\)).*', {}, 0)",
		x_date = r"xfn:search('- (.*)$', string(./title), 0)",
		x_location = r"xfn:search('\)(.*)-', string(./title), 0)",
		t_keep = 0,
		t_update = 0,
	).update())

