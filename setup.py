#!/usr/bin/python3

import getpass, os, configparser
from paths import paths



def check_base_files():
	setup_archives: dict = {
		'dir': "/home/" + getpass.getuser() + "/.config/checkInvest/",
		'config_path': "/home/" + getpass.getuser() + "/.config/checkInvest/checkInvest.config",
		'data_path': "/home/" + getpass.getuser() + "/.config/checkInvest/data.json"
	}
	
	
	if os.path.isfile(setup_archives['config_path']):
		parser: configparser = configparser.ConfigParser()
		parser.read(setup_archives['config_path'])
		if parser['SETUP'].getboolean('INITIAL_SETUP_DONE', False):
			return None

	if not os.path.isdir(setup_archives['dir']):
            	os.mkdir(setup_archives['dir'])
	if not os.path.isfile(setup_archives['data_path']):
		setup_archives['data_file'] = open(setup_archives['data_path'], 'w')
		setup_archives['data_file'].close()
	if not os.path.isfile(setup_archives['config_path']):
		setup_archives['config_file'] = open(setup_archives['config_path'], 'w')
		setup_archives['config_file'].write(\
		"[SETUP]" + "\n" \
		"INITIAL_SETUP_DONE = true" + '\n' \
		"" + '\n' \
		"[PATHS]" + '\n' \
		"SETUP_DIR =" + setup_archives['dir'] + '\n' \
		"CONFIG_FILE =" + setup_archives['config_path']  + '\n' \
		"DATA_FILE =" + setup_archives['data_path'] + '\n') 
		setup_archives['config_file'].close()


def dict_from_parser() -> dict:
	path: str = "/home/" + getpass.getuser() + "/.config/checkInvest/checkInvest.config"
	parser: configparser = configparser.ConfigParser()
	parser.read(path)
	return parser._sections
