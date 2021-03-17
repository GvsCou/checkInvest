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
		self.two_hifen_opts: list = [foo for foo in self.chewing if fnmatch(foo, '--[!-]?*')] if not self.one_hifen_opts else []
		self.list_opts: list = [foo for foo in self.chewing if fnmatch(foo,'as=?*')]
		self.non_opts: list = [foo for foo in self.chewing if foo not in list(chain(self.one_hifen_opts, self.two_hifen_opts, self.list_opts))\
		and not [char for char in list(foo) if char in ["-", "="]]][1:]
	
	def spit(self) -> dict:
		"""Returns a list of arguments tha match one of the values of
		'self.patterns'"""
		if self.one_hifen_opts or self.two_hifen_opts:
			option: str = self.one_hifen_opts.pop(-1) if self.one_hifen_opts else self.two_hifen_opts.pop(-1)	
		else:
			print("No option given")
			exit()
		spat: dict = {
			'opt': option,
			'list_opt': self.list_opts.pop(-1) if self.list_opts else None,
			'args': self.non_opts
		}		

		return spat
		
class SwitchStatement:
	
	def __init__(self, arg1: dict):
		self.spat = arg1
		self.all_options: list = [
				['-le', '--list-entries'],
				['-ld', '--list-data-sets']
		]
	
	def switch(self) -> None:
		default = "Invalid Option"
		case_num: int = sum(i for i in [1 for foo in self.all_options if self.spat['opt'] in foo])
		case_num: int = 1 
		for opts_list in self.all_options:
			if self.spat['opt'] in opts_list:
				case_num -= 1
				break
			else:
				case_num += 1
		getattr(self, "case_" + str(case_num) , lambda: print(default))()
	
	#Lists existing entries
	def case_0(self) -> None:
		optionFunctions.Entry().list_entries()
	
	#Lists existing data sets
	def case_1(self) -> None:
		optionFunctions.DataSet().list_existing()

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
		SwitchStatement(Chewer(sys.argv).spit()).switch()
	else:
		print("No option given")

configOptions.check_base_files()
check_option()
