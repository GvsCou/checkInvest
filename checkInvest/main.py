#!/usr/bin/python3

import sys 
from fnmatch import fnmatch
from itertools import chain
from .optionFunctions import Entry, DataSet, Updater, help_func, ArgHandler
from . import configOptions

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
		"""Returns a list of arguments"""
		if self.one_hifen_opts:
			option: str = self.one_hifen_opts.pop(-1)	
			is_interactive: bool = False
			if list(option).copy().pop(-1) == 'i':
				is_interactive: bool = True
				cleaned_option: str = option[:2]
				option = cleaned_option
		elif self.two_hifen_opts:
			option: str = self.two_hifen_opts.pop(-1)
			is_interactive: bool = False
			if list(option.split('-')).pop(-1) == 'interactive':
				is_interactive: bool = True
				option = option.replace('-interactive', "", 1)
		else:
			print("No option given")
			exit()
		spat: dict = {
			'opt': option,
			'list_opt': self.list_opts.pop(-1)[3:] if self.list_opts else "",
			'args': self.non_opts,
			'i': is_interactive
		}		
		return spat
		
class SwitchStatement:
	
	def __init__(self, arg1: dict):
		self.spat = arg1
		self.all_options: list = [
				['-l', '--list-entries'],
				['-L', '--list-data-sets'],
				['-S', '--show-current-data'],
				['-a', '--add-entry'],
				['-A', '--add-data-set'],
				['-C', '--change-current-data'],
				['-W', '--wipe-data-set'],
				['-D', '--delete-data-set'],
				['-u', '--update-data-set'],
				['-U', '--update-all']
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
		getattr(self, "case_" + str(case_num) , self.default)()
		return None
	
	#Lists existing entries
	def case_0(self) -> None:
		Entry().list_entries(self.spat['args'], self.spat['list_opt'])
		return None
	
	#Lists existing data sets
	def case_1(self) -> None:
		DataSet().list_existing()
		return None
	
	#Shows current data set
	def case_2(self) -> None:
		DataSet().show_current()
		return None
	
	#Adds a new entry
	def case_3(self) -> None:
		if self.spat['i']:
			Entry().add_entry(is_interactive = True)
		else:
			Entry().add_entry(self.spat['args'])
		return None

	#Adds a new data set	
	def case_4(self) -> None:
		DataSet().add_new()

	#Changes current data set
	def case_5(self) -> None:
		DataSet().change_current()
	
	#Wipe a data set
	def case_6(self) -> None:
		DataSet().wipe()

	#Deletes a data set
	def case_7(self) -> None:
		DataSet().delete()
	
	#Updates the current or the selected data sets
	def case_8(self) -> None:
		Updater().update_data_set(self.spat['args'])
	
	#Updates all data sets
	def case_9(self) -> None:
		Updater().update_all()

	#Default (--help)
	def default(self) -> None:
		help_func()


def check_option():
	if len(sys.argv) > 1:
		SwitchStatement(Chewer(sys.argv).spit()).switch()
	else:
		print("No option given")
def main():
	configOptions.check_base_files()
	ArgHandler().add_args()

if __name__=='__main__':
	main()
