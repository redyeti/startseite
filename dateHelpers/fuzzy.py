#-*- coding: utf-8 -*-
import datetime, time, re
import dateutil.parser

weekdayRe = [
	"MO(NTAG)?|MON(DAY)?",
	"DI(ENSTAG)?|TUE(SDAY)?",
	"MI(TTWOCH)?|WED(NESDAY)?",
	"DO(NNERSTAG)?|THU(RSTAY)?",
	"FR(EITAG)?|FRI(DAY)?",
	"SA(MSTAG)?|SAT(URDAY)?",
	"SO(NNTAG)?|SU(NDAY)?",
]
weekdayRe = [re.compile(r"\b(%s)\b" % x) for x in weekdayRe]

offsetRe = [
	U"HEUTE|TODAY",
	U"MORGEN|TOMORROW",
	U"ÜBERMORGEN"
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
	" UM ",
]

timeparts = [
	"%H:%M",
	"%H:%M UHR",
	"%H UHR",
	"%H:%M:%S",
	"%H UHR %M",
	"%H:%M:%S %Z",
]

substitutes = [
	(r"([0-9]+)-[0-9]+ UHR", r"\2 UHR"),
]
substitutes = [(re.compile(r"\b(%s)\b" % x[0]),x[1]) for x in substitutes]

dtformats = []
for datepart in dateparts:
	for connector in connectors:
		for timepart in timeparts:
			dtformats.append(datepart + connector + timepart)


