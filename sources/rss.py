from feedbase import FeedBase

class RSS(FeedBase):
	def findDate(self, item):
		return item.find("./pubDate")

	def findItems(self, doc):
		return doc.findall(".//item")

	def findLink(self, item):
		return item.find("./link")

	def findTitle(self, item):
		return item.find("./title")

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

