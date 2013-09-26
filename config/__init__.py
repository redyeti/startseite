#-*- coding: utf8 -*-
from __future__ import unicode_literals
from nds import NDS
from classManager import ManagedMeta
from dateHelpers import *
import re, datetime, time, os
from scope import scope

class Config(object):
	__metaclass__ = ManagedMeta

	@staticmethod
	def colorize(date, name, location, source, link, marked):
		if source == "1t":
			return "blue"
		return None

	@staticmethod
	def prioritize(date, name, location, source, link, marked):
		"""
		Measure interestingness of the entries. Lowering the score makes entries more interresting.
		"""

		prio = date - time.time()
		
		if source in ("Dota", "Mk I", "Mk II","Mk"):
			if location not in NDS+["Bremen","Hamburg"]:
				return None
			elif location == "Hannover":
				prio -= parseDuration("2 months")

		if source == "Prinz":
			if location in ["Forum","Kamp"]:
				return None

		if marked:
			prio = (prio - parseDuration("1 day")) / 2

		# default
		return prio

	DATABASE_FILE = os.path.dirname(__file__)+"/../db.sqlite"

	def __init__(self):
		globals().update(self._CM)
		type(self).db = self._CM.Database(self.DATABASE_FILE)

		today = datetime.date.today()

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

		@scope
		def _():
			t_week = today + datetime.timedelta(7)
			t_today = today.strftime("%d.%m.%Y")
			t_week = t_week.strftime("%d.%m.%Y")

			RSS(
				name = "Prinz",
				url = "http://hannover.prinz.de/termine/veranstaltungen?search=&primetime=&location_id=&sort=date&main_cat_id=1&hide_form=0&cat_id[0]=1&cat_id[1]=100&cat_id[2]=1214065&cat_id[3]=1214067&cat_id[4]=1214069&cat_id[5]=1291239&date_from=%s&date_to=%s&feed=rss" % (t_today, t_week),
				x_title = r"xfn:search('^(.*\)).*', {}, 0)",
				x_date = r"xfn:search('- (.*)$', string(./title), 0)",
				x_location = r"xfn:search('\)(.*)-', string(./title), 0)",
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

		Atom(
			name = "xkcd",
			url = "http://what-if.xkcd.com/feed.atom",
			t_keep = "8 d",
			t_update = "1 d",
		)



		@scope
		def _():
			t_year = today.strftime("%Y")
			t_nextyear = str(int(t_year)+1)
			mk = Union(
				name = "Mk",
				t_keep = 0,
				t_update = "100 d",
			)
			for y in (t_year, t_nextyear):
				mk.add(
					HTMLFeed,
					url = "http://www.marktkalendarium.de/maerkte%s.php" % y,
					x_items = ".//table[@border=1]//tr[position()>1][not(./td[@colspan])]",
					x_date = "string(./td[1])",
					x_title = "string(./td[3])",
					x_location = r"xfn:search('.-[0-9]+\s(.*)', string(./td[4]), 0)",
					x_link = r"./td[6]//a/@href",
				)


	THEME="sheep"

