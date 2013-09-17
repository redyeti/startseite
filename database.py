import sqlite3
import time
import pickle

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from collections import MutableMapping
from classManager import ManagedMeta

class KeepNone(object):
	def __getitem__(self, fn):
		def _fn(x):
			if x is None:
				return None
			else:
				return fn(x)
		return _fn

KeepNone = KeepNone()

class RegisterView(MutableMapping):
	def __init__(self, db, source):
		self._conn = db._conn
		self.__source = source

	def __delitem__(self, item):
		c = self._conn.cursor()
		c.execute(
			"DELETE FROM registry WHERE source = ? AND key = ?",
			[self.__source, item]
		)

	def __getitem__(self, item):
		c = self._conn.cursor()
		c.execute(
			"SELECT value FROM registry WHERE source = ? AND key = ?",
			[self.__source, item]
		)
		for row in c:
			return pickle.loads(row[0])

	def __iter__(self):
		c = self._conn.cursor()
		c.execute(
			"SELECT key FROM registry WHERE source = ?",
			[self.__source]
		)
		for row in c:
			yield c[0]

	def __len__(self):
		c = self._conn.cursor()
		c.execute(
			"SELECT COUNT(key) FROM registry WHERE source = ?",
			[self.__source]
		)
		for row in c:
			return c[0]

	def __setitem__(self, item, value):
		c = self._conn.cursor()
		c.execute(
			"INSERT OR REPLACE INTO registry (source, key, value) VALUES (?,?,?)",
			[self.__source, item, pickle.dumps(value)]
		)

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
		c = self._conn.cursor()
		c.execute("""
			CREATE TABLE IF NOT EXISTS items (
				id integer PRIMARY KEY AUTOINCREMENT,
				date float NOT NULL,
				name text,
				location text,
				source text NOT NULL,
				link text,
				update_time float NOT NULL,
				hidden bool NOT NULL,
				CONSTRAINT constr_it UNIQUE (date, name, source))
			""")
		c.execute("""
			CREATE TABLE IF NOT EXISTS sources (
				source text NOT NULL UNIQUE,
				last_update float NOT NULL DEFAULT 0,
				update_interval float NOT NULL,
				hide_time float NOT NULL)
			""")
		c.execute("""
			CREATE TABLE IF NOT EXISTS registry (
				source TEXT NOT NULL,
				key text NOT NULL,
				value,
				CONSTRAINT constr_reg UNIQUE (source, key))
			""")

	def getRegister(self, source):
		return RegisterView(self, source)

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
		c = self._conn.cursor()
		c.execute("""
			INSERT OR REPLACE INTO items
			(date, name, location, source, link, update_time, hidden) VALUES (?,?,?,?,?,?,0)
			""", [float(item.date), KeepNone[unicode](item.name), KeepNone[unicode](item.location), source, KeepNone[unicode](item.link), time])
		
	def hideItem(self, item):
		c = self._conn.cursor()
		c.execute("""
			UPDATE items SET hidden = 1 WHERE id = ?
			""", [int(item)])
		self._conn.commit()

	def setSources(self, sources):
		c = self._conn.cursor()
		for name, source in self._CM.Source.sources.iteritems():
			c.execute("""
				INSERT OR IGNORE INTO sources (source, update_interval, hide_time) VALUES (?,?,?)
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
