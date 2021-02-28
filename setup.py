#!/usr/bin/python3

import getpass, os
from paths import paths

config_file_dict: dict = {
        'path': paths['config_file']
}

data_file_dict: dict = {
        'path': paths['data_file']
}

def check_base_files():
	if os.path.isfile(config_file_dict['path']) and os.path.isfile(data_file_dict['path']):
		pass
	else:
		if not os.path.isdir(paths['config_dir']):
            		os.mkdir(paths['config_dir'])
		if not os.path.isfile(data_file_dict['path']):
			data_file_dict['file'] = open(data_file_dict['path'], 'w')
			data_file_dict['file'].close()
		if not os.path.isfile(config_file_dict['path']):
			config_file_dict['file'] = open(config_file_dict['path'],'w')
			config_file_dict['file'].write("[SETUP]" + "\n" \
							"INITIAL_SETUP_DONE = true")
			config_file_dict['file'].close()


check_base_files()
