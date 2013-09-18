#-*- coding: utf-8 -*-
import datetime, time, re
import dateutil.parser
from fuzzy import *

__all__ = ("parseDate","fuzzyParseDate", "parseDuration")

def parseDate(s, formats):
	s = s.strip()
	for f in formats:
		try:
			return time.mktime(time.strptime(s, f))
		except ValueError:
			pass #Sic!
	raise ValueError("No matching time format found: %s, %s" % (repr(s), repr(formats)))

def fuzztime(s):
	try:
		return parseDate(s, dtformats)
	except ValueError:
		try:
			return time.mktime(dateutil.parser.parse(s).timetuple())
		except ValueError:
			raise ValueError("Could not parse date %s" % repr(s))


def fuzzyParseDate(s):

	# substitute expressions

	s = s.lower()
	for reg, rep in substitutes:
		s = reg.sub(rep, s)
	
	today = datetime.date.today()
	for num, reg in enumerate(weekdayRe):
		offset = (num - today.weekday()) % 7
		rdate = today + datetime.timedelta(days=offset)
		s = reg.sub(rdate.isoformat(), s)

	for offset, reg in enumerate(offsetRe):
		rdate = today + datetime.timedelta(days=offset)
		s = reg.sub(rdate.isoformat(), s)
	
	try:
		return fuzztime(s)
	except ValueError:
		if "," in s:
			return fuzztime(s.split(",",1)[1])
		else:
			raise

def parseDuration(time):
	if isinstance(time, float):
		return int(time)
	elif isinstance(time, int):
		return time
	
	time = time.split()
	if len(time) != 2:
		raise ValueError("Time string must consist of a number and a unit separated by whitespace")

	value, unit = time
	value = float(value)
	return parseDurationParts(value, unit)

def parseDurationParts(value, unit):
	if unit in set(("second","seconds","s")):
		return value
	elif unit in set(("minute","minutes","min","m")):
		return parseDurationParts(value*60, "s")
	elif unit in set(("hour","hours","h")):
		return parseDurationParts(value*60, "m")
	elif unit in set(("day","days","d")):
		return parseDurationParts(value*24, "h")
	elif unit in set(("week","weeks","w")):
		return parseDurationParts(value*7, "d")
	elif unit in set(("month","months","M")):
		return parseDurationParts(value*30, "d")
	elif unit in set(("year","years","y","a")):
		return parseDurationParts(value*365, "d")
	else:
		raise ValueError("Invalid unit: "+unit)
