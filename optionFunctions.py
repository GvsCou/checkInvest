#!/usr/bin/python3

import os, sys, json
import entry, setup


def default():
	print("Invalid Option")


def add_entry():
	ticker: str = input("Enter asset name: ")
	path: str = setup.dict_from_parser()['PATHS']['data_file']
	if os.stat(path).st_size == 0:
		entry.add_new(ticker, entry.DICT_MODES.BRAND_NEW)
	else:
		py_dict: dict = entry.get_json(path)
	
		for key in py_dict:
			if key == ticker:
				entry.add_to_old(ticker)
				return None
		
		entry.add_new(ticker)


def list_entries():
	path: str = setup.dict_from_parser()['PATHS']['data_file']

	if os.stat(path).st_size == 0:
		print("There are no entries in the data file")
	elif len(sys.argv) > 2:
		args: list = []

		for i in range(2, len(sys.argv), 1):
			args.append(sys.argv[i].upper())
			
		py_dict = entry.get_json(path)
		for key in py_dict:
			if key in args:
				args.remove(key)
				print("Entries for " + key + ":" + '\n\n' \
				+ json.dumps(py_dict[key], indent=2, sort_keys=True) + '\n\n')

		unfound: int = len(args)
		if unfound != 0:
			for foo in args:
				print(foo + " was not found among the entries" + '\n')
	else:
		py_dict: dict = entry.get_json(path)
		print(json.dumps(py_dict, indent=2, sort_keys=True))
		



