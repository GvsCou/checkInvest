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
			'config_path': "/home/" + getuser() + "/.config/checkInvest/checkInvest.cfg",
			'data_sets_path': "/home/" + getuser() + "/.config/checkInvest/data_sets.json",
			'data_sets_dir':  "/home/" + getuser() + "/.config/checkInvest/dataSets/",
			'update_file': "/home/" + getuser() + "/.config/checkInvest/update_file.json"
		}	
	elif user_os == "Windows":
		paths_dict = {
			'dir': "C:\\Users\\" + getuser() + "\\AppData\\Local\\checkInvest\\",
			'config_path': "C:\\Users\\" + getuser() + "\\AppData\\Local\\checkInvest\\checkInvest.cfg",
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
	
	#Checks if initial set up is done by getting the bool var from parser['SETUP']['INITIAL_SETUP_DONE']
	try:
		parser: configparser = configparser.ConfigParser()
		parser.read(setup_archives['config_path'])	
		if parser['SETUP'].getboolean('INITIAL_SETUP_DONE', False):
			return None
	except:	
		#Makes dir for config and data files
		os.mkdir(setup_archives['dir'])
		
		if not os.path.isfile(setup_archives['data_sets_path']):
			#Makes dir for dataSetN.json
			os.mkdir(setup_archives['data_sets_dir']) 

			#Creates dataSet1.json (alias="Default")
			with open(setup_archives['data_sets_path'], 'w') as ds_file:
				data_sets: dict = data_set_dir("data_set_1", "Default", setup_archives['data_sets_dir'] + 
				"dataSet1.json", is_current=True)
				json.dump(data_sets, ds_file, sort_keys = True, indent = 2)

			#Creates data_sets.json which contains the path, alias and current (bool) of
			#all created data sets
			data_set_1: file = open(data_sets['data_sets']['data_set_1']['path'], 'w')
			data_set_1.close()

		#Creates checkInvest.config	and exits the program printing a message of initial set up done
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
				"[CURRENT_DATA_SET]" + '\n' \
				"PATH =" + setup_archives['data_sets_dir'] + "dataSet1.json" + '\n' \
				"ALIAS = Default" + '\n') 
			print("Initial set up done; run checkinv -h/--help to know what you can do")
			exit()

#Transforms the info from .config in a dict
def dict_from_parser() -> dict:
	path: str = set_paths_dict()['config_path']
	parser: configparser = configparser.ConfigParser()
	parser.read(path)
	return parser._sections
