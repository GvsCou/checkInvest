#!/usr/bin/python3

import sys, entry, os, configparser, json
import setup, optionFunctions


def switch(option: str):
	def add_entry():
		ticker: str = input("Enter asset name: ")
		path: str = setup.dict_from_parser()['PATHS']['data_file']

		if os.stat(path).st_size == 0:
			entry.add_new(ticker, entry.DICT_MODES.BRAND_NEW)
			return None	
		else:
			py_dict: dict = entry.get_json(path)
		
			for key in py_dict:
				if key == ticker:
					entry.add_to_old(ticker)
					return None
		
			entry.add_new(ticker)

	def default():
		print("Invalid Option")


	cases: dict = {
		'a': add_entry,
		'l': optionFunctions.list_entries
	}

	cases.get(option, default)()


def one_hifen(option: str):
	if option[0] == "-" and len(option) > 1 and option[1] != "-":
		switch(option[1])
	else:
		print("Invalid Option")

def check_option():
	if len(sys.argv) > 1:
		one_hifen(sys.argv[1])
	else:
		print("Unrecognized Option")

setup.check_base_files()
check_option()
