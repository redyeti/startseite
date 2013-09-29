#!/usr/bin/env python
import argparse
import inspect

# --- dependency injection ---
import database
import source
import config
import worker
from sources import *
from classManager import ManagedMeta, ClassManager
ClassManager.Config()

parser = argparse.ArgumentParser(description='Infoserver commandline tool. Note that all commands are processed in commandline order.')

class CallbackAction(argparse.Action):
	def __init__(self, callback, *args,**params):
		nargs = len(inspect.getargspec(callback).args)
		self.__callback = callback
		argparse.Action.__init__(self,nargs=nargs-1, *args,**params)

	def __call__(self, parser, namespace, values, option_string=None):
		self.__callback(namespace, *values)

class Action(object):
	def __init__(self, group, *args, **params):
		self.__group = group
		self.__args = args
		self.__params = params

	def __call__(self, fn):
		self.__group.add_argument(*self.__args,action=CallbackAction,callback=fn,**self.__params)

sourceCommands = parser.add_argument_group('Source Commands')
workerCommands = parser.add_argument_group('Worker Commands')

@Action(sourceCommands, "-i",'--invalidate',metavar="NAME", help='Invalidate the source NAME')
def invalidate(namespace, i):
	ClassManager.Config.db.invalidateSource(i)

@Action(workerCommands, "-w",'--run-worker', help='Run the worker once')
def invalidate(namespace):
	ClassManager.Worker(nofail=False).runOnce()

@Action(workerCommands, "-W",'--run-worker-nofail', help='Run the worker once with catchall enabled')
def invalidate(namespace):
	ClassManager.Worker(nofail=True).runOnce()

args = parser.parse_args()
print args

