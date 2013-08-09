#!/usr/bin/env python
from BaseHTTPServer import  BaseHTTPRequestHandler, HTTPServer
from ajaxManager import AjaxManager
from pprint import pprint
import os, sys
import config

class Handler(AjaxManager, BaseHTTPRequestHandler):

	def __init__(self, *args, **params):
		AjaxManager.__init__(self, config.DATABASE)
		BaseHTTPRequestHandler.__init__(self, *args, **params)

	def do_GET(self, *args, **params):
		#print "GET:", self.path

		if self.path == "/":
			self.__do_default()
			return
	
		namespaces = self.path.split("/",2)
		if hasattr(self, "_Handler__do_"+namespaces[1]):
			getattr(self, "_Handler__do_"+namespaces[1])(namespaces[2])
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
		path = os.path.join(self.getPath(), "helper", request)
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
