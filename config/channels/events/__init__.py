from channel import Channel
from sources import *

@Channel.factory(Union, t_keep = 0, t_update = "100 d")
def marktkalendarium(mk):
	import datetime
	today = datetime.date.today()
	t_year = today.strftime("%Y")
	t_nextyear = str(int(t_year)+1)
	for y in (t_year, t_nextyear):
		mk.add(
			HTMLFeed,
			url = "http://www.marktkalendarium.de/maerkte%s.php" % y,
			x_items = ".//table[@border=1]//tr[position()>1][not(./td[@colspan])]",
			x_date = "string(./td[1])",
			x_title = "xfn:br2x(./td[3],' ')",
			x_location = r"xfn:search('.-[0-9]+\s(.*)', string(./td[4]), 0)",
			x_link = r"./td[6]//a/@href",
		)
	return mk
