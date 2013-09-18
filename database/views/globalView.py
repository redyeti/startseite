from collections import MutableMapping
import pickle

class GlobalView(MutableMapping):
	def __init__(self, db):
		self._conn = db._conn

	def __delitem__(self, item):
		with self._conn:
			self._conn.execute(
				"DELETE FROM global WHERE key = ?",
				[item]
			)

	def __getitem__(self, item):
		c = self._conn.cursor()
		c.execute(
			"SELECT value FROM global WHERE key = ?",
			[item]
		)
		try:
			return pickle.loads(c.fetchone()[0])
		except TypeError:
			raise KeyError("Key %s not found." % item)

	def __iter__(self):
		c = self._conn.cursor()
		c.execute(
			"SELECT key FROM global",
			[self.__source]
		)
		return [x[0] for x in c.fetchall()]

	def __len__(self):
		c = self._conn.cursor()
		c.execute(
			"SELECT COUNT(key) FROM global",
			[self.__source]
		)
		for row in c:
			return c[0]

	def __setitem__(self, item, value):
		with self._conn:
			self._conn.execute(
				"INSERT OR REPLACE INTO global (key, value) VALUES (?,?)",
				[item, pickle.dumps(value)]
			)
