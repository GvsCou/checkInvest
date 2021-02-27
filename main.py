#!/usr/bin/python3

import sys, entry
from paths import paths

def switch(option: str):
	def add_entry():
		ticker: str = input("Enter asset name: ")
		py_dict: dict = entry.get_json(paths['data_file'])
		
		for key in py_dict:
			if key == ticker:
				entry.add_to_old(ticker)
				return None
		
		entry.add_new(ticker)

	def default():
		print("Invalid Option")


	cases: dict = {
		'a': add_entry
	}

	cases.get(option, default)()


if sys.argv[1][0] == "-" and len(sys.argv[1]) > 1:
	switch(sys.argv[1][1])

