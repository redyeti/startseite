from sources import *
from nds import NDS

DATABASE = "db.sqlite"

SOURCES = dict(
	dota = Dota(t_update="1 month", t_keep=0)
)

def prioritize(date, name, location, source, link):

	if source == "dota" and location not in NDS+["Bremen","Hamburg"]:
		return None

	# default
	return date
