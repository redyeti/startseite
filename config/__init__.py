#-*- coding: utf8 -*-
from __future__ import unicode_literals
from nds import NDS
from classManager import ManagedMeta

D = 60*60*24
W = 7*D
M = 30*D

class Config(object):
	__metaclass__ = ManagedMeta

	@staticmethod
	def prioritize(date, name, location, source, link):

		if source == "Dota":
			if location not in NDS+["Bremen","Hamburg"]:
				return None
			elif location == "Hannover":
				return date - 2*M

		# default
		return date

	DATABASE_FILE = "db.sqlite"

	def __init__(self):
		globals().update(self._CM)

		Diff(name="KP", t_update="10 min", t_keep="10 h", url="http://kamelopedia.mormo.org/index.php/Spezial:Letzte_%C3%84nderungen")
		Dota(name="Dota", t_update="1 d", t_keep=0)


	THEME="sheep"
