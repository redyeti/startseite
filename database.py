import sqlite3
import config
import time

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class Database(object):
	def __init__(self, filename):
		self.__conn = sqlite3.connect(filename)
		self.__conn.row_factory = sqlite3.Row
		self.__conn.create_function("PRIORITIZE", 5, config.prioritize)
		c = self.__conn.cursor()
		self.initTables()

	def initTables(self):
		c = self.__conn.cursor()
		c.execute("""
			CREATE TABLE IF NOT EXISTS items (
				id integer PRIMARY KEY AUTOINCREMENT,
				date float NOT NULL,
				name text,
				location text,
				source text NOT NULL,
				link text,
				update_time float NOT NULL,
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


	def getCurrentItems(self):
		c = self.__conn.cursor()
		now = time.time()
		c.execute("""
			SELECT *
			FROM items
			JOIN sources USING(source)
			WHERE ? < hide_time + date
			AND PRIORITIZE(date, name, location, source, link) IS NOT NULL
			ORDER BY PRIORITIZE(date, name, location, source, link) ASC
			LIMIT 15
			""", [now])
		for row in c:
			yield row

	def addItem(self, time, source, item):
		c = self.__conn.cursor()
		c.execute("""
			INSERT OR REPLACE INTO items
			(date, name, location, source, link, update_time) VALUES (?,?,?,?,?,?)
			""", [float(item.date), unicode(item.name), unicode(item.location), source, item.link, time])
		

	def setSources(self, sources):
		c = self.__conn.cursor()
		for name, source in sources.iteritems():
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

	def updateSource(self, name, time):
		c = self.__conn.cursor()
		c.execute("""
			UPDATE sources SET last_update = ? WHERE source = ?
			""", [time, name])
		#TODO: delete items if no longer on the list and source.delete_old == True
		self.__conn.commit()
		
		
	def getOutOfDateSources(self):
		c = self.__conn.cursor()
		c.execute("""
			SELECT source 
			FROM sources
			WHERE last_update + update_interval < ?
			""", [time.time()])
		for row in c:
			yield (row[0], config.SOURCES[row[0]])
