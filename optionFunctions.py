#!/usr/bin/python3

import os, sys, json
import entry
from paths import paths

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
		



