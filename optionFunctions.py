#!/usr/bin/python3

import os, sys, json
import entry, setup

def list_entries():
	path: str = setup.dict_from_parser()['PATHS']['data_file']
	if os.stat(path).st_size == 0:
		print("No entries found")
	elif len(sys.argv) > 3:
		print("Too many arguments")
	elif len(sys.argv) > 2:
		py_dict: dict = entry.get_json(path)[sys.argv[2]]
		print("Entries for " + sys.argv[2] + ":" + '\n\n' + json.dumps(py_dict, indent=2, sort_keys=True)) 
	else:
		py_dict: dict = entry.get_json(path)
		print(json.dumps(py_dict, indent=2, sort_keys=True))
		



