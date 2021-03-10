#!/usr/bin/python3

import os, sys, json, configparser, fnmatch
import configOptions
from subFunctions import entry, dataSet, listModes




def add_entry():
	ticker: str = input("Enter asset name: ")
	path: str = configOptions.dict_from_parser()['DATA_SET']['current']
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
	path: str = configOptions.dict_from_parser()['DATA_SET']['current']
	args: list = [] if len(sys.argv) < 3 else [foo for foo in sys.argv[2:] if not fnmatch.fnmatch(foo, 'as=?*')]
	possible_modes: list = fnmatch.filter(sys.argv, 'as=?*')

	def switch_list(option: str, tickers: list):
		cases: dict = {
			'json': listModes.json_mode
		}
		cases.get(option, listModes.table_mode)(tickers)

	if os.stat(path).st_size == 0:
		print("There are no entries in the data file")
	else:
		mode: str = possible_modes.pop(-1)[3:] if len(possible_modes) > 0 else ""
		switch_list(mode, args)


def data_base():
	data_sets_paths: str = configOptions.dict_from_parser()['PATHS']['data_sets_file']
	data_sets_dir: str = configOptions.dict_from_parser()['PATHS']['data_sets_dir']
	all_data_sets: dict = entry.get_json(data_sets_paths)
	
	
	def add_new(alias: str):
		py_dict: dict = all_data_sets
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
		print(alias + " was created and is now the new current data set")

		

	if len(sys.argv) > 2:
		aliases: list = dataSet.get_existing_aliases()
		args: list = sys.argv
		del args[0:2]
		for arg in args:
			if arg in aliases:
				dataSet.change_current(arg)
			else:
				add_new(arg)
					
	else: #show current data set
		for key in all_data_sets:
			for key2 in all_data_sets[key]:
				if all_data_sets[key][key2].get('current', False):
					print("Current data set: " + all_data_sets[key][key2].get('alias', "Not Found"))
					return None

def list_data_sets():
	path: str = configOptions.dict_from_parser()['PATHS']['data_sets_file']
	if os.stat(path).st_size == 0:
		print("There are no data sets")
	else:
		py_dict: dict = entry.get_json(path)
		aliases: list = []
		for key in py_dict:
			for key2 in py_dict[key]:
				aliases.append(py_dict[key][key2].get('alias'))
		for i in range(0, len(aliases), 1):
			print(str(i) + ": " + aliases[i]) 

def remove_data_base():
	if len (sys.argv) < 3:
		print("No data set given")
		return None
	data_sets_paths: str = configOptions.dict_from_parser()['PATHS']['data_sets_file']
	alias: str = sys.argv[2]
	file_path: str = ""
	all_data_sets: dict = entry.get_json(data_sets_paths)
	
	if alias == "Default":
		print("You can neither delete 'Default' nor have zero data sets")
		return None
	else:
		for key in list(all_data_sets):
			for key2 in list(all_data_sets[key]):
				if alias == all_data_sets[key][key2].get('alias', ""):
					file_path = all_data_sets[key][key2]['path']
					os.remove(file_path)
					if all_data_sets[key][key2].get('current', False): 
						dataSet.change_current('Default')
					new_set_dict: dict = entry.get_json(data_sets_paths)
					del new_set_dict[key][key2]
					entry.dump_json(data_sets_paths, new_set_dict)
					print(alias + " deleted")
					return None
						
		print("'" + alias + "' not found")

def clean_data_base():
	data_sets_file_path: str = configOptions.dict_from_parser()['PATHS']['data_sets_file']
	data_sets_dict: dict = entry.get_json(data_sets_file_path)
	
	if len(sys.argv) < 3:
		print("No data set specified")
	else:
		for alias in sys.argv[2:]:
			for key in data_sets_dict:
				for key2 in data_sets_dict[key]:
					if data_sets_dict[key][key2].get('alias', "") == alias:	
						data_set: file = open(data_sets_dict[key][key2]['path'], 'w')
						data_set.truncate(0)
						data_set.close()


def default():
	print("Invalid Option")

