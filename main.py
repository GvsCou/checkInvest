#!/usr/bin/python3

import sys, entry, os, configparser, json
import setup
from paths import paths

def switch(option: str):
	def add_entry():
		ticker: str = input("Enter asset name: ")

		if os.stat(paths['data_file']).st_size == 0:
			entry.add_new(ticker, entry.DICT_MODES.BRAND_NEW)
			return None	
		else:
			py_dict: dict = entry.get_json(paths['data_file'])
		
			for key in py_dict:
				if key == ticker:
					entry.add_to_old(ticker)
					return None
		
			entry.add_new(ticker)

	def list_entries():
		if os.stat(paths['data_file']).st_size == 0:
			print("No entries found")
		elif len(sys.argv) > 3:
			print("Too many arguments")
		elif len(sys.argv) > 2:
			py_dict: dict = entry.get_json(paths['data_file'])[sys.argv[2]]
			print("Entries for " + sys.argv[2] + ":" + '\n\n' + json.dumps(py_dict, indent=2, sort_keys=True)) 
		else:
			py_dict: dict = entry.get_json(paths['data_file'])
			print(json.dumps(py_dict, indent=2, sort_keys=True))
			

	def default():
		print("Invalid Option")


	cases: dict = {
		'a': add_entry,
		'l': list_entries
	}

	cases.get(option, default)()


def check_init_setup():
	if not os.path.isfile(paths['config_file']):
		setup.check_base_files()

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

check_init_setup()
check_option()
