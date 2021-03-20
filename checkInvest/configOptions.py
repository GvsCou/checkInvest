import os, configparser, json
from platform import system
from getpass import getuser

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

def set_paths_dict() -> dict:
	user_os: str = system()
	paths_dict: dict = {}
	
	if user_os == "Linux":
		paths_dict = {
			'dir': "/home/" + getuser() + "/.config/checkInvest/",
			'config_path': "/home/" + getuser() + "/.config/checkInvest/checkInvest.config",
			'data_sets_path': "/home/" + getuser() + "/.config/checkInvest/data_sets.json",
			'data_sets_dir':  "/home/" + getuser() + "/.config/checkInvest/dataSets/",
			'update_file': "/home/" + getuser() + "/.config/checkInvest/update_file.json"
		}	
	elif user_os == "Windows":
		paths_dict = {
			'dir': "C:\\Users\\" + getuser() + "\\AppData\\Local\\checkInvest\\",
			'config_path': "C:\\Users\\" + getuser() + "\\AppData\\Local\\checkInvest\\checkInvest.config",
			'data_sets_path': "C:\\Users\\" + getuser() + "\\AppData\\Local\\checkInvest\\data_sets.json",
			'data_sets_dir':  "C:\\Users\\" + getuser() + "\\AppData\\Local\\checkInvest\\dataSets\\",
			'update_file': "C:\\Users\\" + getuser() + "\\AppData\\Local\\checkInvest\\update_file.json"
		}
	else:
		print("Unsupported OS")
		exit()
	return paths_dict

def check_base_files():
	setup_archives: dict = set_paths_dict()
	
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
		with open(setup_archives['config_path'], 'w') as setup_archives['config_file']:
			setup_archives['config_file'].write(\
			"[SETUP]" + "\n" \
			"INITIAL_SETUP_DONE = true" + '\n' \
			"BASE_CURRENCY = USD" + '\n' \
			"" + '\n' \
			"[PATHS]" + '\n' \
			"SETUP_DIR =" + setup_archives['dir'] + '\n' \
			"CONFIG_FILE =" + setup_archives['config_path']  + '\n' \
			"DATA_SETS_FILE =" + setup_archives['data_sets_path'] + '\n' \
			"DATA_SETS_DIR =" + setup_archives['data_sets_dir'] + '\n' \
			"UPDATE_FILE =" + setup_archives['update_file'] + '\n' \
			"" + '\n' \
			"[DATA_SET]" + '\n' \
			"CURRENT =" + setup_archives['data_sets_dir'] + "dataSet1.json" + '\n') 


def dict_from_parser() -> dict:
	path: str = "/home/" + getuser() + "/.config/checkInvest/checkInvest.config"
	parser: configparser = configparser.ConfigParser()
	parser.read(path)
	return parser._sections