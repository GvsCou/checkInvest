#!/usr/bin/python3

import sys
import setup, optionFunctions


def switch(option: str):

	cases: dict = {
		'a': optionFunctions.add_entry,
		'le': optionFunctions.list_entries,
		'd': optionFunctions.data_base,
		'ld': optionFunctions.list_data_sets,
		'rd': optionFunctions.remove_data_base
	}

	cases.get(option, optionFunctions.default)()


def one_hifen(option: str):
	if option[0] == "-" and len(option) > 1 and option[1] != "-":
		switch(option[1:])
	else:
		print("Invalid Option")

def check_option():
	if len(sys.argv) > 1:
		one_hifen(sys.argv[1])
	else:
		print("Unrecognized Option")

setup.check_base_files()
check_option()
