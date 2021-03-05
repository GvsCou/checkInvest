import configparser
from . import entry
import setup

def get_existing_aliases() -> list:
	data_sets: dict = entry.get_json(setup.dict_from_parser()['PATHS']['data_sets_file'])
	aliases: list = []
	for key in data_sets:
		for key2 in data_sets[key]:
			aliases.append(data_sets[key][key2].get('alias', None))
	data_sets.clear()
	return aliases


def get_path(alias: str) -> str:
	data_sets: dict = entry.get_json(setup.dict_from_parser()['PATHS']['data_sets_file'])
	path: str = ""
	for key in data_sets:
		for key2 in data_sets[key]:
			if data_sets[key][key2].get('alias', "") == alias:
				path = 	data_sets[key][key2].get('path', "")
				break
	data_sets.clear()
	return path


def config_set_current(path: str):
	
	parser: configparser = configparser.ConfigParser()
	parser.read(setup.dict_from_parser()['PATHS']['config_file'])
	parser.set('DATA_SET', 'current', path)
	config_file: file = open(setup.dict_from_parser()['PATHS']['config_file'], 'w')
	parser.write(config_file)
	config_file.close()


def change_current(new_current: str):
		#change .config
		path: str = get_path(new_current)	
		config_set_current(path)
		data_sets_paths: str = setup.dict_from_parser()['PATHS']['data_sets_file']
		#change data_sets
		py_dict: dict = entry.get_json(data_sets_paths)
		for key in list(py_dict):
			for key2 in list(py_dict[key]):
				if py_dict[key][key2].get('alias', "") == new_current:
					 py_dict[key][key2]['current'] = True
				else:
					py_dict[key][key2]['current'] = False
		entry.dump_json(data_sets_paths, py_dict)
		print(new_current + " is the new current data set")


