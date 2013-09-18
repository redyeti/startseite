import abc
from collections import namedtuple
import time
from classManager import ManagedABCMeta
from dateHelpers import *

__all__ = ("InsertEntry", "parseDate", "Source", "CleanOldEntries")

# an entry to insert into the database
InsertEntry = namedtuple("Entry","date name location link")

# clean old entries from previous updates no longer in the list
class CleanOldEntries(object):
	__slots__ = []

class Source(object):
	__metaclass__ = ManagedABCMeta

	@abc.abstractmethod
	def update(self):
		pass

	sources = {}

	def __init__(self, name, t_update, t_keep):
		self.__t_update = parseDuration(t_update)
		self.__t_keep = parseDuration(t_keep)
		self.__name = name

		self.registry = self.database.getRegistryView(name)
		self.sources[name] = self

	@property
	def database(self):
		return self._CM.Config.db

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

