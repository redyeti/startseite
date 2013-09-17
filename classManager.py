from collections import Mapping
import abc

class ClassManager(Mapping):
	__classes = {}

	def add(self, c):
		print "ADDING:", c, c.__name__
		self.__classes[c.__name__] = c

	def __getattr__(self, attr):
		return self.__classes[attr]

	def __getitem__(self, item):
		return self.__classes[item]

	def __iter__(self):
		return iter(self.__classes)

	def __len__(self):
		return len(self.__classes)

ClassManager = ClassManager()

class ManagedMeta(type):
	def __init__(cls, name, bases, dct):
		super(ManagedMeta, cls).__init__(name, bases, dct)
		ClassManager.add(cls)
		cls._CM = ClassManager

class ManagedABCMeta(ManagedMeta, abc.ABCMeta):
	pass
