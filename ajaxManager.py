import os 
from collections import namedtuple

from wheezy.template.engine import Engine
from wheezy.template.ext.core import CoreExtension
from wheezy.template.loader import FileLoader

from database import Database

searchpath = [os.path.dirname(__file__)+'/templates']
engine = Engine(
    loader=FileLoader(searchpath),
    extensions=[CoreExtension()]
)

import time


try:
    from wheezy.html.utils import escape_html as escape
except ImportError:
    import cgi
    escape = cgi.escape
import json

def formatTime(t):
	tm = time.localtime(t)
	if tm.tm_min == 0 and tm.tm_hour == 0:
		return time.strftime("%d.%m.%Y",tm)
	else:
		return time.strftime("%d.%m.%Y %H:%M", tm)

engine.global_vars.update({
	'h': lambda x: escape(str(x)),
	'j': json.dumps,
	't': formatTime,
})

class Entry(object):
	def __init__(self, **params):
		self.__dict__.update(params)

	def createHTMLTools():
		return ""

class AjaxManager(object):
	def __init__(self,db):
		self.db = Database(db)

	def getPath(self):
		return os.path.dirname(__file__)

	def template(self, template, **params):

		t = engine.get_template(template+".html")
		return t.render(params)		
		
	def ajax(self, call):
		if hasattr(self, "_AjaxManager__"+call):
			return getattr(self, "_AjaxManager__"+call)()
		else:
			raise Exception()


	def __getItems(self):
		data = dict(entries=self.db.getCurrentItems())
		return self.template("items", **data)
