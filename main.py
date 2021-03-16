#!/usr/bin/python3

import sys 
from fnmatch import fnmatch
import configOptions, optionFunctions


def switch(option: str):

	cases: dict = {
		'a': optionFunctions.Entry().add_entry,
		'le': optionFunctions.Entry().list_entries,
		'ad': optionFunctions.DataSet().add_new,
		'cd': optionFunctions.DataSet().change_current,
		'sd': optionFunctions.DataSet().show_current	
		#'ld': optionFunctions.list_data_sets,
		#'rd': optionFunctions.remove_data_base,
		#'cd': optionFunctions.clean_data_base
	}

	cases.get(option, optionFunctions.default)()


def one_hifen(option: str):
	if fnmatch(option, '-[!-]*'):
		switch(option[1:])
	else:
		print("Invalid Option")

def check_option():
	if len(sys.argv) > 1:
		one_hifen(sys.argv[1])
	else:
		print("No option given")

configOptions.check_base_files()
check_option()
