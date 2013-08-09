# -*- coding: utf8 -*-
import re

re_link = re.compile(ur"\[\[([^\]]+\|)?([^\]]+)\]\]")
url = "http://de.wikipedia.org/w/index.php?title=Liste_der_Städte_und_Gemeinden_in_Niedersachsen&action=raw"
import os
__all__ = ["NDS"]

# extracted from http://de.wikipedia.org/w/index.php?title=Liste_der_Städte_und_Gemeinden_in_Niedersachsen
path = os.path.dirname(__file__)
wpname = os.path.join(path,"nds.wiki")

if os.path.isfile(wpname):
	with open(wpname) as f:
		data = f.read()
else:
	import urllib2
	data = urllib2.urlopen(url).read()
	with open(wpname,"w") as f:
		f.write(data)



NDS = [x[1] for x in re_link.findall(data)]
