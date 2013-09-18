#!/usr/bin/env python
from BaseHTTPServer import  BaseHTTPRequestHandler, HTTPServer
from ajaxManager import AjaxManager
import cgi
from pprint import pprint
import os, sys

import config
import database
from sources import *
from classManager import ManagedMeta, ClassManager
ClassManager.Config()

class Handler(AjaxManager, BaseHTTPRequestHandler):

	def __init__(self, *args, **params):
		AjaxManager.__init__(self,
			self._CM.Config.DATABASE_FILE,
			self._CM.Config.prioritize
		)
		BaseHTTPRequestHandler.__init__(self, *args, **params)

	def do_GET(self, *args, **params):

		if self.path == "/":
			self.__do_default()
			return
	
		namespaces = self.path.split("/",2)
		if hasattr(self, "_Handler__do_"+namespaces[1]):
			getattr(self, "_Handler__do_"+namespaces[1])(namespaces[2])
			return

		print self.headers

		self.__do_error(400)

	def do_POST(self, *args, **params):

		ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
		if ctype == 'multipart/form-data':
			self.postvars = cgi.parse_multipart(self.rfile, pdict)
		elif ctype == 'application/x-www-form-urlencoded':
			length = int(self.headers.getheader('content-length'))
			self.postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
		else:
			self.postvars = {}

		namespaces = self.path.split("/",2)
		if namespaces[1] == "ajax":
			self.__do_ajax(namespaces[2])
			return

		self.__do_error(400)

	def __do_default(self):
		self.send_response(200)
		self.end_headers()
		self.wfile.write(self.template("index"))

	def __do_ajax(self, request):
		data = self.ajax(request)
		self.send_response(200)
		self.end_headers()
		self.wfile.write(data)

	def __do_helper(self, request):
		path = os.path.join(self.getPath(), "themes", self._CM.Config.THEME, "helper", request)
		if os.path.isfile(path):
			try:
				with open(path) as f:
					data = f.read()
			except:
				self.__do_error()
				raise
		
			self.send_response(200)
			self.end_headers()
			self.wfile.write(data)
		else:
			self.__do_error(404)


	def __do_error(self, code=500):
		self.send_error(code)
		#self.send_header("Content-type", "text/html")
		#self.end_headers()
		#self.wfile.write("blu<b>bb</b>!")
		if code == 500:
			raise

def runServer():
	server_address = ('', 8023)
	httpd = HTTPServer(server_address, Handler)
	while True:
		httpd.handle_request()

if __name__ == "__main__":
	runServer()
