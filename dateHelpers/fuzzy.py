#-*- coding: utf-8 -*-
import datetime, time, re
import dateutil.parser

weekdayRe = [
	"mo(ntag)?|mon(day)?",
	"di(enstag)?|tue(sday)?",
	"mi(ttwoch)?|wed(nesday)?",
	"do(nnerstag)?|thu(rstay)?",
	"fr(eitag)?|fri(day)?",
	"sa(mstag)?|sat(urday)?",
	"so(nntag)?|su(nday)?",
]
weekdayRe = [re.compile(r"\b(%s)\b" % x) for x in weekdayRe]

offsetRe = [
	u"heute|today",
	u"morgen|tomorrow",
	u"übermorgen"
]
offsetRe = [re.compile(r"\b(%s)\b" % x) for x in offsetRe]

dateparts = [
	"%Y-%m-%d",
	"%d.%m.%Y",
	"%d.%m.%y",
	"%d.%m.",
	"%d %b %Y",
]

connectors = [
	" ",
	" um ",
]

timeparts = [
	"%H:%M",
	"%H:%M uhr",
	"%H uhr",
	"%H:%M:%S",
	"%H uhr %M",
	"%H:%M:%S %Z",
]

substitutes = [
	(r"([0-9]+)-[0-9]+ uhr", r"\2 uhr"),
]
substitutes = [(re.compile(r"\b(%s)\b" % x[0]),x[1]) for x in substitutes]

dtformats = []
for datepart in dateparts:
	for connector in connectors:
		for timepart in timeparts:
			dtformats.append(datepart + connector + timepart)


