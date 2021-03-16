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
		one_hifen(sys.argv[1])
	else:
		print("No option given")

configOptions.check_base_files()
check_option()
