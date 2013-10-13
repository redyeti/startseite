from channel import Channel
from sources import *

Channel("whatif", Atom,
	url = "http://what-if.xkcd.com/feed.atom",
	t_keep = "8 d",
	t_update = "1 d",
)
