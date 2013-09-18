#-*- coding: utf8 -*-
from __future__ import unicode_literals
from nds import NDS
from classManager import ManagedMeta
from dateHelpers import *
import re, datetime

class Config(object):
	__metaclass__ = ManagedMeta

	@staticmethod
	def prioritize(date, name, location, source, link):
		"""
		Measure interestingness of the entries. Lowering the score makes entries more interresting.
		"""

		if source == "Dota":
			if location not in NDS+["Bremen","Hamburg"]:
				return None
			elif location == "Hannover":
				return date - parseDuration("2 months")

		if source == "Prinz":
			if location in ["Forum","Kamp"]:
				return None

		# default
		return date

	DATABASE_FILE = "db.sqlite"

	def __init__(self):
		globals().update(self._CM)
		type(self).db = self._CM.Database(self.DATABASE_FILE, self.prioritize)

		#Diff(
		#	name = "KP",
		#	t_update = "10 min",
		#	t_keep="10 h",
		#	url="http://kamelopedia.mormo.org/index.php/Spezial:Letzte_%C3%84nderungen"
		#)

		Dota(
			name="Dota",
			 t_update="1 d",
			 t_keep=0
		)

		today = datetime.date.today()
		t_week = today + datetime.timedelta(7)
		today = today.strftime("%d.%m.%Y")
		t_week = t_week.strftime("%d.%m.%Y")

		RSS(
			name = "Prinz",
			url = "http://hannover.prinz.de/termine/veranstaltungen?search=&primetime=&location_id=&sort=date&main_cat_id=1&hide_form=0&cat_id[0]=1&cat_id[1]=100&cat_id[2]=1214065&cat_id[3]=1214067&cat_id[4]=1214069&cat_id[5]=1291239&date_from=%s&date_to=%s&feed=rss" % (today, t_week),
			title = re.compile(r"^(.*\))"),
			date = re.compile(r"- (.*)$"),
			location = re.compile(r"\)(.*)-"),
			t_keep = 0,
			t_update = "1 d",
		)

		RSS(
			name = "1t",
			url = "http://mediathek.daserste.de/export/rss?sendung=4326",
			grep = "tagesschau",
			delete = True,
			n_keep = 1,
			t_keep = "1 d",
			t_update = "1 h",
		)


	THEME="sheep"

