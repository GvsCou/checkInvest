#!/usr/bin/python3

import getpass, os, configparser, json

def data_set_dir(key: str, alias: str, path: str, is_current=False) -> dict:
	new_dict: dict = {
		'data_sets': {
				key: {
					'path': path,
					'alias': alias,
					'current': is_current
				}
			}
		}
	return new_dict


def check_base_files():
	setup_archives: dict = {
		'dir': "/home/" + getpass.getuser() + "/.config/checkInvest/",
		'config_path': "/home/" + getpass.getuser() + "/.config/checkInvest/checkInvest.config",
		'data_sets_path': "/home/" + getpass.getuser() + "/.config/checkInvest/data_sets.json",
		'data_sets_dir':  "/home/" + getpass.getuser() + "/.config/checkInvest/dataSets/",
	}
	
	
	if os.path.isfile(setup_archives['config_path']):
		parser: configparser = configparser.ConfigParser()
		parser.read(setup_archives['config_path'])
		if parser['SETUP'].getboolean('INITIAL_SETUP_DONE', False):
			return None
	
	os.mkdir(setup_archives['dir'])
	
	if not os.path.isfile(setup_archives['data_sets_path']):
		os.mkdir(setup_archives['data_sets_dir'])
		setup_archives['data_sets_file'] = open(setup_archives['data_sets_path'], 'w')
		data_sets: dict = data_set_dir("data_set_1", "Default", setup_archives['data_sets_dir'] + 
		"dataSet1.json", is_current=True)
		json.dump(data_sets, setup_archives['data_sets_file'], sort_keys = True, indent = 2)
		data_set_1: file = open(data_sets['data_sets']['data_set_1']['path'], 'w')
		setup_archives['data_sets_file'].close()
		data_set_1.close()

	if not os.path.isfile(setup_archives['config_path']):
		setup_archives['config_file'] = open(setup_archives['config_path'], 'w')
		setup_archives['config_file'].write(\
		"[SETUP]" + "\n" \
		"INITIAL_SETUP_DONE = true" + '\n' \
		"BASE_CURRENCY = usd" + '\n' \
		"" + '\n' \
		"[PATHS]" + '\n' \
		"SETUP_DIR =" + setup_archives['dir'] + '\n' \
		"CONFIG_FILE =" + setup_archives['config_path']  + '\n' \
		"DATA_SETS_FILE =" + setup_archives['data_sets_path'] + '\n' \
		"DATA_SETS_DIR =" + setup_archives['data_sets_dir'] + '\n' \
		"" + '\n' \
		"[DATA_SET]" + '\n' \
		"CURRENT =" + setup_archives['data_sets_dir'] + "dataSet1.json" + '\n') 
		setup_archives['config_file'].close()


def dict_from_parser() -> dict:
	path: str = "/home/" + getpass.getuser() + "/.config/checkInvest/checkInvest.config"
	parser: configparser = configparser.ConfigParser()
	parser.read(path)
	return parser._sections
