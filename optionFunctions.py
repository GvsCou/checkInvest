#!/usr/bin/python3

import os, sys, json, configparser
import setup
from scriptsOpt import entry, dataSet




def add_entry():
	ticker: str = input("Enter asset name: ")
	path: str = setup.dict_from_parser()['DATA_SET']['current']
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
	path: str = setup.dict_from_parser()['DATA_SET']['current']

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


def data_base():
	data_sets_paths: str = setup.dict_from_parser()['PATHS']['data_sets_file']
	data_sets_dir: str = setup.dict_from_parser()['PATHS']['data_sets_dir']
	all_data_sets: dict = entry.get_json(data_sets_paths)
	
	
	def add_new(alias: str):
		py_dict: dict = entry.get_json(setup.dict_from_parser()['PATHS']['data_sets_file'])
		i: int = 0
		for key in list(py_dict):
			for key2 in list(py_dict[key]):
				i += 1
				if py_dict[key][key2].get('current', False):
					 py_dict[key][key2]['current'] = False

		py_dict['data_sets']['data_set_' + str(i + 1)] = {
						'alias': alias,
						'current': True,
						'path': data_sets_dir + "dataSet" + str(i + 1) + ".json"
		}
		
		entry.dump_json(data_sets_paths, py_dict)
		new_data_file: file = open(py_dict['data_sets']['data_set_' + str(i + 1)]['path'], 'w')
		new_data_file.close()
		dataSet.config_set_current(py_dict['data_sets']['data_set_' + str(i + 1)]['path'])
	

	def change_current(new_current: str):
		#change .config
		path: str = dataSet.get_path(new_current)	
		dataSet.config_set_current(path)
		#change data_sets
		py_dict: dict = entry.get_json(setup.dict_from_parser()['PATHS']['data_sets_file'])
		for key in list(py_dict):
			for key2 in list(py_dict[key]):
				if py_dict[key][key2].get('alias', "") == new_current:
					 py_dict[key][key2]['current'] = True
				else:
					py_dict[key][key2]['current'] = False
		entry.dump_json(data_sets_paths, py_dict)
		print(new_current + " is the new current data set")

	if len(sys.argv) > 2:
		aliases: list = dataSet.get_existing_aliases()
		args: list = sys.argv
		del args[0:2]
		for arg in args:
			if arg in aliases:
				change_current(arg)
			else:
				add_new(arg)
					
	else: #show current data set
		for key in all_data_sets:
			for key2 in all_data_sets[key]:
				if all_data_sets[key][key2].get('current', False):
					print("Current data set: " + all_data_sets[key][key2].get('alias', "Not Found"))
					return None

def default():
	print("Invalid Option")

