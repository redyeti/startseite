import sqlite3
import time

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from classManager import ManagedMeta
from views.registryView import RegistryView
from views.globalView import GlobalView

class KeepNone(object):
	def __getitem__(self, fn):
		def _fn(x):
			if x is None:
				return None
			else:
				return fn(x)
		return _fn

KeepNone = KeepNone()


class Database(object):
	__metaclass__ = ManagedMeta

	def __init__(self, filename, prio):
		self._conn = sqlite3.connect(filename)
		self._conn.row_factory = sqlite3.Row
		self._conn.create_function("PRIORITIZE", 5, prio)
		self._conn.isolation_level = None
		c = self._conn.cursor()
		self.initTables()

	def initTables(self):
		with self._conn:
			self._conn.execute("pragma foreign_keys=ON")
			self._conn.execute("""
				CREATE TABLE IF NOT EXISTS items (
					id integer PRIMARY KEY AUTOINCREMENT,
					date float NOT NULL,
					name text,
					location text,
					source text NOT NULL REFERENCES sources(source) ON DELETE cascade,
					link text,
					update_time float NOT NULL,
					hidden bool NOT NULL,
					CONSTRAINT constr_it UNIQUE (date, name, source))
				""")
			self._conn.execute("""
				CREATE TABLE IF NOT EXISTS sources (
					source text NOT NULL UNIQUE,
					last_update float NOT NULL DEFAULT 0,
					update_interval float NOT NULL,
					hide_time float NOT NULL)
				""")
			self._conn.execute("""
				CREATE TABLE IF NOT EXISTS registry (
					source TEXT NOT NULL REFERENCES sources(source) ON DELETE cascade,
					key text NOT NULL,
					value text,
					CONSTRAINT constr_reg UNIQUE (source, key))
				""")
			self._conn.execute("""
				CREATE TABLE IF NOT EXISTS global (
					key text NOT NULL UNIQUE,
					value text)
				""")

	def getRegistryView(self, source):
		return RegistryView(self, source)

	def getGlobalView(self):
		return GlobalView(self)

	def getCurrentItems(self):
		c = self._conn.cursor()
		now = time.time()
		c.execute("""
			SELECT *, PRIORITIZE(date, name, location, source, link) AS priority
			FROM items
			JOIN sources USING(source)
			WHERE hidden = 0
			AND ? < hide_time + date
			AND PRIORITIZE(date, name, location, source, link) IS NOT NULL
			ORDER BY PRIORITIZE(date, name, location, source, link) ASC
			LIMIT 15
			""", [now])
		for row in c:
			yield row

	def addItem(self, time, source, item):
		with self._conn:
			c = self._conn.cursor()
			c.execute("""
				INSERT OR IGNORE INTO items
				(date, name, location, source, link, update_time, hidden) VALUES (?,?,?,?,?,?,0)
				""", [float(item.date), KeepNone[unicode](item.name), KeepNone[unicode](item.location), source, KeepNone[unicode](item.link), time])
			if c.rowcount <= 1:
				c.execute("""
					UPDATE items SET location = ?, link = ?, update_time = ? WHERE date = ? AND name = ? AND source = ?
					""", [KeepNone[unicode](item.location), KeepNone[unicode](item.link), time, float(item.date), KeepNone[unicode](item.name), source])
		
	def hideItem(self, item):
		with self._conn:
			self._conn.execute("""
				UPDATE items SET hidden = 1 WHERE id = ?
				""", [int(item)])

	def setSources(self, sources):
		with self._conn:
			c = self._conn.cursor()
			for name, source in self._CM.Source.sources.iteritems():
				c.execute("""
					INSERT OR IGNORE INTO sources (source, last_update, update_interval, hide_time) VALUES (?,0,?,?)
				""", [name, source.t_update, source.t_keep])

				if c.rowcount <= 1:
					c.execute("""
						UPDATE sources SET update_interval=?, hide_time=? WHERE source=?
					""", [source.t_update, source.t_keep, name])
					

			n = ",".join(["?"]*len(sources))
			c.execute("""
				DELETE FROM sources WHERE source NOT IN (""" + n + """)
			""", list(sources))

	def cleanOldEntries(self, source, updateTime):
		c = self._conn.cursor()
		c.execute("""
			DELETE FROM items WHERE source = ? AND update_time < ?
			""", [source, updateTime])
		self._conn.commit()
		

	def updateSource(self, name, time):
		c = self._conn.cursor()
		c.execute("""
			UPDATE sources SET last_update = ? WHERE source = ?
			""", [time, name])
		self._conn.commit()
		
	def getLastUpdate(self):
		c = self._conn.cursor()
		c.execute(
			"SELECT MAX(last_update) FROM sources",
		)
		return c.fetchone()[0]
		
	def getOutOfDateSources(self):
		c = self._conn.cursor()
		c.execute("""
			SELECT source 
			FROM sources
			WHERE last_update + update_interval < ?
			""", [time.time()])
		for row in c:
			yield (row[0], self._CM.Source.sources[row[0]])

	def commit(self):
		pass
		#self._conn.commit()
