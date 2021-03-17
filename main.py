#!/usr/bin/python3

import sys 
from fnmatch import fnmatch
from itertools import chain
import configOptions, optionFunctions

class Chewer:
	"""Class responsible for chewing user input and spitting it in a usable state
	for the optionFunctions.py classes"""
	
	def __init__(self, arg1: list):
		self.chewing: list = arg1

		self.one_hifen_opts: list = [foo for foo in self.chewing if fnmatch(foo, '-[!-]*')]
		self.two_hifen_opts: list = [foo for foo in self.chewing if fnmatch(foo, '--[!-]?*')]
		self.list_opts: list = [foo for foo in self.chewing if fnmatch(foo,'as=?*')]
		self.non_opts: list = [foo for foo in self.chewing if foo not in list(chain(self.one_hifen_opts, self.two_hifen_opts, self.list_opts))\
		and not [char for char in list(foo) if char in ["-", "="]]][1:]
	
	def spit(self, patt: str="non") -> list:
		"""Returns a list of arguments tha match one of the values of
		'self.patterns'"""

		return getattr(self, patt + "_opts")
		



def switch(option: str):

	cases: dict = {
		'a': optionFunctions.Entry().add_entry,
		'le': optionFunctions.Entry().list_entries,
		'ad': optionFunctions.DataSet().add_new,
		'cd': optionFunctions.DataSet().change_current,
		'sd': optionFunctions.DataSet().show_current,
		'ld': optionFunctions.DataSet().list_existing,
		'rd': optionFunctions.DataSet().remove,
		'C': optionFunctions.DataSet().clean
	}

	cases.get(option, optionFunctions.default)()


def one_hifen(option: str):
	if fnmatch(option, '-[!-]*'):
		switch(option[1:])
	else:
		print("Invalid Option")

def check_option():
	if len(sys.argv) > 1:
		chewer = Chewer(sys.argv)	
		print(chewer.spit("one_hifen"))
		print(chewer.spit("two_hifen"))
		print(chewer.spit("list"))
		print(chewer.spit())
	else:
		print("No option given")

configOptions.check_base_files()
check_option()
