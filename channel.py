import inspect

class Channel(object):
	def __init__(self, name, src, **defaultparams):

		if isinstance(name, basestring):
			module = inspect.getmodule(inspect.stack()[1][0])
			setattr(module, name, self)
		elif callable(name):
			name = name.__name__
			module = inspect.getmodule(inspect.stack()[2][0])
		else:
			raise TypeError("Invalid name/callable")

		print "M:", module.__name__

		nameprefix = module.__name__.split(".",2)[2]
		fullname = "#%s.%s" % (nameprefix, name)

		self.__src = src
		self.__defaultparams = dict(name=fullname)
		self.__defaultparams.update(defaultparams)
		self.fn = lambda x:x

	def __call__(self, **arguments):
		args = self.__defaultparams.copy()
		args.update(arguments)

		return self.fn(self.__src(**args))


	@classmethod
	def factory(cls, src, **params):
		def _factory(fn):
			c = cls(fn, src, **params)
			c.fn = fn
			return c
		return _factory
