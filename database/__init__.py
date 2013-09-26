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

	def __init__(self, filename):
		self._conn = sqlite3.connect(filename)
		self._conn.row_factory = sqlite3.Row
		self._conn.create_function("PRIORITIZE", 6, self._CM.Config.prioritize)
		self._conn.create_function("COLORIZE", 6, self._CM.Config.colorize)
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
					marked bool NOT NULL,
					CONSTRAINT constr_it UNIQUE (date, name, source))
				""")
			self._conn.execute("""
				CREATE TABLE IF NOT EXISTS sources (
					source text NOT NULL UNIQUE,
					last_update float NOT NULL DEFAULT 0,
					update_interval float,
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
			SELECT
				*,
				PRIORITIZE(date, name, location, source, link, marked) AS priority,
				COLORIZE(date, name, location, source, link, marked) AS color
			FROM items
			JOIN sources USING(source)
			WHERE hidden = 0
			AND ? < hide_time + date
			AND PRIORITIZE(date, name, location, source, link, marked) IS NOT NULL
			ORDER BY PRIORITIZE(date, name, location, source, link, marked) ASC
			LIMIT 15
			""", [now])
		for row in c:
			yield row

	def addItem(self, time, source, item):
		with self._conn:
			self.upsert(
				"items",
				dict(date=float(item.date), name=KeepNone[unicode](item.name), source=source),
				dict(location=KeepNone[unicode](item.location), link=KeepNone[unicode](item.link), update_time=time, hidden=0, marked=0),
				dict(location=KeepNone[unicode](item.location), link=KeepNone[unicode](item.link), update_time=time)
			)
		
	def hideItem(self, item):
		with self._conn:
			self._conn.execute("""
				UPDATE items SET hidden = 1 WHERE id = ?
				""", [int(item)])
		
	def unmarkItem(self, item):
		with self._conn:
			self._conn.execute("""
				UPDATE items SET marked = 1 WHERE id = ?
				""", [int(item)])
	def markItem(self, item):
		with self._conn:
			self._conn.execute("""
				UPDATE items SET marked = 0 WHERE id = ?
				""", [int(item)])

	def debugSources(self):
		c = self._conn.cursor()
		c.execute("""
			SELECT *
			FROM sources
			""")
		for row in c:
			print "Source", row


	def debugSelect(self, name):
		c = self._conn.cursor()
		c.execute("""
			SELECT * FROM sources WHERE source=?
		""", [name])
		for row in c:
			print "Sel", row

	def upsert(self, table, keys, insert, update):
		c = self._conn.cursor()

		ik, iv = zip(*(keys.items()+insert.items()))
		insertString = "INSERT INTO `%s` (%s) VALUES (%s)" % (table, ",".join(ik), ",".join(["?"]*len(iv)))
		try:
			# insert
			c.execute(insertString, list(iv))
		except sqlite3.IntegrityError:
			# update instead
			updateString = "UPDATE `%s` SET %s WHERE %s" % (table, ", ".join([x+" = ?" for x in update.keys()]), " AND ".join([x+" = ?" for x in keys.keys()]))
			c.execute(updateString, list(update.values()+keys.values()))

	def setSources(self, sources):
		with self._conn:
			c = self._conn.cursor()
			for name, source in self._CM.Source.sources.iteritems():
				self.upsert(
					"sources",
					dict(source=name),
					dict(last_update=0, update_interval=source.t_update, hide_time=source.t_keep),
					dict(update_interval=source.t_update, hide_time=source.t_keep),
				)


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

	def invalidateSource(self, name):
		self.updateSource(name, 0)
		
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
		self._conn.commit()
		#pass

	def rollback(self):
		self._conn.rollback()
		#pass
