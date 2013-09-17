import abc
from collections import namedtuple
import time
from classManager import ManagedABCMeta

__all__ = ("InsertEntry", "parseDate", "Source", "CleanOldEntries")

# an entry to insert into the database
InsertEntry = namedtuple("Entry","date name location link")

# clean old entries from previous updates no longer in the list
class CleanOldEntries(object):
	__slots__ = []

def parseDate(s, formats):
	s = s.strip()
	for f in formats:
		try:
			return time.mktime(time.strptime(s, f))
		except ValueError:
			pass #Sic!
	raise ValueError("No matching time format found: %s, %s" % (repr(s), repr(formats)))

class Source(object):
	__metaclass__ = ManagedABCMeta

	@abc.abstractmethod
	def update(self):
		pass

	sources = {}

	def __init__(self, name, t_update, t_keep):
		self.__t_update = self.__parseTime(t_update)
		self.__t_keep = self.__parseTime(t_keep)
		self.__name = name

		if not hasattr(self, "database"):
			Source.database = self._CM.Database(
				self._CM.Config.DATABASE_FILE,
				self._CM.Config.prioritize
			)

		self.registry = self.database.getRegister(name)
		self.sources[name] = self

	@property
	def name(self):
		return self.__name

	@property
	def t_update(self):
		return self.__t_update

	@property
	def t_keep(self):
		return self.__t_keep

	def __hash__(self):
		return hash((self.__class__.__name__, self.name))

	def __parseTime(self, time):
		if isinstance(time, float):
			return int(time)
		elif isinstance(time, int):
			return time
		
		time = time.split()
		if len(time) != 2:
			raise ValueError("Time string must consist of a number and a unit separated by whitespace")

		value, unit = time
		value = float(value)
		return self.__resolveTime(value, unit)
	
	def __resolveTime(self, value, unit):
		if unit in set(("second","seconds","s")):
			return value
		elif unit in set(("minute","minutes","min","m")):
			return self.__resolveTime(value*60, "s")
		elif unit in set(("hour","hours","h")):
			return self.__resolveTime(value*60, "m")
		elif unit in set(("day","days","d")):
			return self.__resolveTime(value*24, "h")
		elif unit in set(("week","weeks","w")):
			return self.__resolveTime(value*7, "d")
		elif unit in set(("month","months","M")):
			return self.__resolveTime(value*30, "d")
		elif unit in set(("year","years","y","a")):
			return self.__resolveTime(value*365, "d")
		else:
			raise ValueError("Invalid unit: "+unit)
