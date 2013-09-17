import os 
from collections import namedtuple

from wheezy.template.engine import Engine
from wheezy.template.ext.core import CoreExtension
from wheezy.template.loader import FileLoader

# --- dependency inhection
import database
import config
from classManager import ClassManager, ManagedMeta

searchpath = [os.path.join(os.path.dirname(__file__),'themes',ClassManager.Config.THEME,'templates')]
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
	'f': lambda x: str(float(x))
})

class Entry(object):
	def __init__(self, **params):
		self.__dict__.update(params)

	def createHTMLTools():
		return ""

class AjaxManager(object):
	__metaclass__ = ManagedMeta

	def __init__(self,db, prio):
		self.db = self._CM.Database(db, prio)

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
		if self.command != "GET":
			return ""

		data = dict(entries=self.db.getCurrentItems())
		return self.template("items", **data)

	def __hideItem(self):
		if self.command != "POST" or 'id' not in self.postvars:
			return ""

		self.db.hideItem(int(self.postvars['id'][0]))
		
