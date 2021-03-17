#!/usr/bin/python3

import sys 
from fnmatch import fnmatch
import configOptions, optionFunctions

class Chewer:
	"""Class responsible for chewing user input and spitting it in a usable state
	for the optionFunctions.py classes"""
	
	def __init__(self, arg1: list):
		self.chewing: list = arg1
		self.patterns: dict = {
				'op_1_h': '-[!-]*',
				'op_2_h': '--[!-]?*',
				'l_op': 'as=?*'
		}
	
	def spit(self, patt: str) -> list:
		"""Returns a list of arguments tha match one of the values of
		'self.patterns'"""

		return [foo for foo in self.chewing if fnmatch(foo, self.patterns.get(patt, None))]
		



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
		pass
	else:
		print("No option given")

configOptions.check_base_files()
check_option()
