from source import *

class Union(Source):
	def __init__(self, **params):
		Source.__init__(self, **params)
		self.__num = 0
		self.__members = []

	def add(self, source, **params):
		s = source(
			name = "%s.union._%i" % (self.name, len(self.__members)),
			t_update = None,
			t_keep = 0,
			**params
		)
		self.__members.append(s)
		return self

	def update(self):
		for member in self.__members:
			 for item in member.update():
				yield item
