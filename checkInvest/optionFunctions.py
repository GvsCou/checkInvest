import os, sys, configparser, fnmatch, enum, datetime
import argparse
from json import load, dump
from . import configOptions
from cryptonator import get_available_currencies, get_exchange_rate
from yahooquery import Ticker


class ArgHandler:
	"""Class responsible for dealing with user input (sys.argv)"""

	def __init__(self):
		self.js = JsonHandler() 				#See JsonHandler Class
		self.cfg: dict = configOptions.dict_from_parser()	#Dict from 'checkInvest.config'
		self.ds_summ: dict = self.js.get_json(			#Dict from 'data_sets.json'
		self.cfg['PATHS']['data_sets_file']
		)['data_sets']

	

	##Adding Arguments##
	
	def handle(self) -> None:
		#Setting Up Parser
		parser = argparse.ArgumentParser(
			prog="checkinv", 						#Name to Be Displayed in --help
			description="A CTL for managing one's expenses and investments", #Description to Be Displayed in --help
			epilog="As a rule of thumb, when an option is captalized (e. g., '-A'), 'tis related to data "
			"set opertations."
		)
		#List Entries
		parser.add_argument(
			'-l', '--list-entries', 		#Name/Flags
			action='store',				#What It Does with Given Arguments
			nargs='*',				#Possible Given Arguments
			help="lists all or some (specified) " 	#Help Message to Be Displayed in --help
			"assets from the current data set",
			metavar="ASSET"				#Metavar to Be Displayed in --help	
		)
		#List Data Sets
		parser.add_argument(
			'-L', '--list-data-sets',
			action='store_true',
			help="lists all existing data sets"
		)
		#Choose display style
		parser.add_argument(
			'-s','--style',
			action='store',
			nargs='?',
			type=str,
			const="",
			choices=['json', ""],
			help="sets the style of the output"
		)
		#Show Current Data Set
		parser.add_argument(
			'-S', '--show-current',
			action='store_true',
			help='shows the current data set'
		)
		#Add a New Entry to Current Data Set
		parser.add_argument(
			'-a', '--add-entry',
			action='store',
			nargs='*',
			type=str,
			help="adds a new entry to the current data set",
			metavar="TICKER PRICE QUANTITY"
		)
		#Add New Data Set
		parser.add_argument(
			'-A', '--add-data-set',
			action='store',
			nargs=1,
			type=str,
			help="adds a new data set",
			metavar="ALIAS"
		)
		#Change Current Data Set
		parser.add_argument(
			'-C', '--change-current',
			action='store',
			nargs=1,
			type=str,
			help="changes the current data set",
			metavar="ALIAS"
		)
		#Wipe Data Set Clean
		parser.add_argument(
			'-W', '--wipe-data-set',
			action='store',
			nargs='+',
			type=str,
			help="wipes a data set clean",
			metavar="ALIAS"
		)
		#Deletes a Data Set
		parser.add_argument(
			'-D', '--delete-data-set',
			action='store',
			nargs='+',
			type=str,
			help="deletes a data set",
			metavar="ALIAS"
		)
		#Update Data Sets
		parser.add_argument(
			'-U', '--update-data-set',
			action='store',
			nargs='+',
			type=str,
			help="updates data sets",
			metavar="ALIAS"
		)
		#Interactive Mode
		parser.add_argument(
			'-i', '--interactive',
			action='store_true',
			help="implements interactive mode"
		)


		##Get all 'add_arguments' given to parser##
		#d: list= parser.__dict__['_optionals'].__dict__['_group_actions']
		#opts: list = []
		#for elem in d:
			#if "_HelpAction" in str(elem):
				#continue
			#else:
				#opts.append(str(elem).replace("_StoreAction", "").split(", ")[1])
		#for i in range(len(opts)):
			#for s in ["'", "--", "]"]:
				#opts[i].replace(s, "")
				#print(i)
				#print(s)
				#print(opts[i])
		#print(opts)
				
		args = parser.parse_args().__dict__

		used_args: dict = {}
		
		for arg in args:
			if args[arg] != None and args[arg] != False:
				used_args[arg] = args[arg] 

		SwitchStatement(used_args).switch()

		return None

class SwitchStatement:
	
	def __init__(self, arg1: dict):
		self.parsed_args = arg1
		self.all_options: list = [
				"list_entries",
				"list_data_sets",
				"show_current",
				"add_entry",
				"add_data_set",
				"change_current",
				"wipe_data_set",
				"delete_data_set",
				"update_data_set"
		]
		
	
	def switch(self) -> None:
		case_num: int = 1 
		for arg in self.all_options:
			try:
				if arg == list(self.parsed_args.keys()).pop(0):
					case_num -= 1
					break
				else:
					case_num += 1
			except:
				print("No argument given; run 'checkinv -h/--help to know what you can do")
				exit()
		getattr(self, "case_" + str(case_num) , lambda: None)()
		return None
	
	#Lists existing entries
	def case_0(self) -> None:
		Entry().list_entries(self.parsed_args['list_entries'], \
		self.parsed_args['style'] if 'style' in self.parsed_args else "")
		return None
	
	#Lists existing data sets
	def case_1(self) -> None:
		DataSet().list_existing()
		return None
	
	#Shows current data set
	def case_2(self) -> None:
		DataSet().show_current()
		return None
	
	#Adds a new entry
	def case_3(self) -> None:
		Entry().add_entry(self.parsed_args['add_entry'],\
		self.parsed_args['interactive'] if 'interactive' in self.parsed_args else False)
		return None

	#Adds a new data set	
	def case_4(self) -> None:
		DataSet().add_new(self.parsed_args['add_data_set'].pop(-1))
		return None

	#Changes current data set
	def case_5(self) -> None:
		DataSet().change_current(self.parsed_args['change_current'].pop(-1))
		return None
	
	#Wipe a data set
	def case_6(self) -> None:
		DataSet().wipe(self.parsed_args['wipe_data_set'])

	#Deletes a data set
	def case_7(self) -> None:
		DataSet().delete(self.parsed_args['delete_data_set'])
	
	#Updates the current or the selected data sets
	def case_8(self) -> None:
		Updater().update_data_set(self.parsed_args['update_data_set'])
	
class JsonHandler:
	"""Simple class that handles getting a dict from a .json and outputting a dict to a .json """

	def get_json(self, path: str) -> dict:
		"""Returns a dict from a .json"""

		with open(path, 'r') as r_file:
			py_dict: dict = load(r_file)

		return py_dict
		

	def dump_json(self, path: str, py_dict: dict, indentation: int=2):
		"""Outputs a .json"""

		with open(path, 'w') as w_file:
			dump(py_dict, w_file, indent=indentation)

##########################################################################################################################

class Asset:
	"""Class responsible for getting the current data for a given asset"""

	def __init__(self, arg1: str, rounding: int=2):
		self.json_handler = JsonHandler()
		self.ticker: str = arg1
		self.currency: str = configOptions.dict_from_parser()['SETUP']['base_currency']
		self.rounding: int = rounding

	def get_grapheme(self) -> str:
		abs_path: str = os.path.realpath(__file__).replace(os.path.basename(__file__),"")
		return "$" if self.currency not in self.json_handler.get_json(abs_path + "currency-format.json") \
		else self.json_handler.get_json(abs_path + "currency-format.json")[self.currency]['symbol'].get('grapheme', "$")

	def get_qtd(self) -> float:
		current_data: dict = self.json_handler.get_json(configOptions.dict_from_parser()['DATA_SET']['current'])
		for key in current_data:
			qtd: float = 0.0
			if key != self.ticker:
				continue
			else:
				for entry in current_data[key]:
					qtd += current_data[key][entry].get('quantity', 0.0)	
				break
					
		return round(qtd, 8)

	def get_price(self) -> float:
		return round(float(self.get_non_crypto(self.ticker, self.currency)), self.rounding) \
	 	if self.ticker not in get_available_currencies() \
		else round(get_exchange_rate(self.ticker.lower(), self.currency.lower()),2)

	def get_non_crypto(self, ticker: str, base_currency: str) -> float:
		"""This functions uses the 'yahooquery' module, when 'ticker' is not in 
		get_available_currencies() - see __init__(): self.price"""
		asset: Ticker = Ticker(ticker)
		#Appends '.sa' if the stock is brazillian
		if "Quote not found for ticker symbol: {}".format(ticker.upper()) in asset.price[ticker]:
			ticker += ".sa"
			asset = Ticker(ticker)		
		#print(asset.price[ticker])	
		given_currency: str = asset.price[ticker].get('currency', "")
		if given_currency != base_currency:
			asset_price: float = 0.0  if given_currency not in get_available_currencies() \
			else get_exchange_rate(given_currency.lower(), self.currency.lower()) * \
			asset.price[ticker].get('regularMarketPrice', 0.0)
		else:
			asset_price: float = asset.price[ticker].get('regularMarketPrice', 0.0)

		return asset_price	

##########################################################################################################################

class Updater:
	"""Class responsible for updating the file the contains the assets' prices"""
	
	def __init__(self):
		self.config_file: dict = configOptions.dict_from_parser()
		self.json_handler = JsonHandler()
		self.ds_dict: dict = self.json_handler.get_json(self.config_file['PATHS']['data_sets_file'])['data_sets']
		self.update_file_path: str = self.config_file['PATHS']['update_file']
		if not os.path.isfile(self.update_file_path):
			self.update_file: file = open(self.update_file_path, 'w')
			self.update_file.close()


	def fill_empty(self, assets: list) -> None:
		py_dict: dict = {}
		for elem in assets:
			py_dict[elem] = Asset(elem).get_price()
			print("{} updated".format(elem))
		self.json_handler.dump_json(self.update_file_path, py_dict)
		return None

	def fill_non_empty(self, assets: list) -> None:
		update_file_dict: dict = self.json_handler.get_json(self.update_file_path)	
		for elem in assets:
			update_file_dict[elem] = Asset(elem).get_price()
			print("{} updated".format(elem))
		self.json_handler.dump_json(self.update_file_path, update_file_dict)
		return None

	def add_asset(self, asset: str) -> None:
		price: float = 0.0		
		if os.stat(self.update_file_path).st_size == 0:
			self.fill_empty([asset])
		else:
			self.fill_non_empty([asset])
		return None

	def update_data_set(self, data_sets: list) -> None:
		"""Function responsible for updating the current data set - if no argument is given - 
		or the given data sets"""

		non_empty_data: list = []
		present_assets: list = []
		for key in self.ds_dict:
			if self.ds_dict[key].get('alias', "") in data_sets:
				if os.stat(self.ds_dict[key]['path']).st_size != 0:
					non_empty_data.append(self.ds_dict[key]['alias'])
					[present_assets.append(foo) for foo in \
					self.json_handler.get_json(self.ds_dict[key]['path'])\
					if foo not in present_assets]
					
		if not non_empty_data:
			print("No valid data set found")
			exit()
		
		if os.stat(self.update_file_path).st_size == 0:
			self.fill_empty(present_assets)
		else:
			self.fill_non_empty(present_assets)
		if data_sets != non_empty_data:
			print("{} not found or empty".format(", ".join([foo for foo in data_sets \
			if foo not in non_empty_data])))
		return None
	
##########################################################################################################################
	
class Entry:
	"""Class responsible for adding, listing and removing entries"""

	def __init__(self):
		self.json_handler = JsonHandler()
		self.config_dict: dict = configOptions.dict_from_parser()
		self.current_path: str = self.config_dict['DATA_SET']['current']

	def add_entry(self, data: list, is_interactive: bool):
		"""Adds a new entry to the current data set, by finding out if it's empty (except),
		if the given ticker already exists as key (try: [...] if ticker in py_dict:...) or
		if the given ticker is a new key (try: [...] else:...)
		"""
		#This if-else statements is responsible to define if there should be or not
		#interactive mode (if is_interactive or not data:...)
		if is_interactive or not data:
			ticker: str = input("Enter the asset name: ").upper()
			price: float = float(input("Enter the asset's price: ").replace(",","."))
			quantity: float = float(input("Enter the asset's quantity: ").replace(",","."))
		elif len(data) < 3:
			print("In non-interactive mode, you must enter these arguments in the following order: " + 
			"ticker, price, quantity")
			exit()
		else:
			ticker: str = data[0].upper()
			price: float = float(data[1].replace(",","."))
			quantity: float = float(data[2].replace(",","."))

		#Dict that will an existing one (try) or a brand new one (except)
		py_dict: dict = {}	
		try:
			#Gets current data set as a dict
			py_dict = self.json_handler.get_json(self.current_path)

			#Checks if the ticker is already a key in py_dict,
			#so that it can act accordingly to add it to the data set
			if ticker in py_dict:
				#Gets all entries of the ticker as a dict
				ticker_entries: dict = py_dict[ticker]
				#Gets number of entries to append it + 1 to the new 'entry_N' key
				entries_num: int = len(ticker_entries.keys())		
				#Adds a new entry with the price (data[1]), quantity (data[2]) and date
				ticker_entries['entry_{}'.format(entries_num + 1)] = {
															'price': price,
															'quantity': quantity,
															'date': str(datetime.date.today())
				}
				#Substitutes old dict (py_dict[ticker]) with a new one (ticker_entries)
				py_dict[ticker] = ticker_entries
			else:
				#Adds ticker as a new key to py_dict
				py_dict[ticker] = {
								 'entry_1': {
									'price': price,
									'quantity': quantity,
									'date': str(datetime.date.today())	
								}
				}
		except:
			#Dumps a completly new dict on current dataSetN
			py_dict = {
					ticker: {
						'entry_1': {
							'price': price,
							'quantity': quantity,
							'date': str(datetime.date.today())
						}
					}
			}

		#Dumps changed or new py_dict in current dataSetN
		self.json_handler.dump_json(self.current_path, py_dict)


	def table_mode(self, tickers: list) -> None:
		"""This function is responsible for displaying the assets, their quantity, current price and value
		as a table"""

		py_dict: dict = self.json_handler.get_json(self.current_path)
		found: bool = True
		not_found_list: list = []
		
	
		if tickers:
			found = False
			for ticker in tickers:
				if ticker not in py_dict:
					not_found_list.append(ticker)
				else:
					found = True
		if found:
			print("{:.<15}{:.<15}{:.<15}Value".format("Ticker","Quantity", "Price"))


		def new_ticker(new_ticker: str, asset_class) -> float:
			Updater().add_asset(ticker)
			
			return asset_class.get_price()

		for ticker in py_dict:
			if tickers and ticker not in tickers:
				continue 
			asset = Asset(ticker)
			grapheme: str = asset.get_grapheme()
			qtd: float = asset.get_qtd()
			#Gets a dict from all the prices in the update_file.json
			try:
				price_dict: dict = self.json_handler.get_json(self.config_dict['PATHS']['update_file'])
			except:
				price_dict: dict = {}	
			price: float = price_dict[ticker] if ticker in price_dict \
			else new_ticker(ticker, asset)
			print("{:<15}{:<15}{:<15}".format(ticker, str(qtd), "{} ".format(grapheme) + \
			str(price)) + "{} ".format(grapheme) + str(round(qtd * price, 2)))
	
		if not_found_list:
			print("")
			for ticker in not_found_list:
				print(ticker + " not found")

	def json_mode(self, tickers: list):
		"""Prints the complete data set in json format"""

		path: str = self.current_path
		py_dict: dict = self.json_handler.get_json(path)
		not_found_list: list = []
		print(json.dumps(py_dict, indent=2, sort_keys=True))

	def list_entries(self, given_tickers: list, mode: str):
		"""Lists the entries of the current data set as a table (table_mode()) or as the other supported
		formats:
		1) json(json_mode())"""
	
		def switch_list(option: str, tickers: list):
			cases: dict = {
				'json': self.json_mode
			}
			cases.get(option, self.table_mode)(tickers)
	
		if os.stat(self.current_path).st_size == 0:
			print("There are no entries in the data file")
		else:
			switch_list(mode, given_tickers)

##########################################################################################################################

class DataSet:
	"""Class responsible for data set operations, like adding, deleting and clearing"""
	
	class __DataSetInner:
		"""Inner Class that has some functions related to the upper class main ones"""

		def __init__(self, adsp:str, ad: dict, js=JsonHandler()):
			self.all_dss: dict = ad
			self.dss_paths: str = adsp
			self.json_handler = js
		
		def get_existing_aliases(self) -> list:
			aliases: list = []
			for key in self.all_dss:
				for key2 in self.all_dss[key]:
					aliases.append(self.all_dss[key][key2].get('alias', None))
			return aliases

		def get_path(self, alias: str) -> str:
			path: str = ""
			for key in self.all_dss:
				for key2 in self.all_dss[key]:
					if self.all_dss[key][key2].get('alias', "") == alias:
						path = self.all_dss[key][key2].get('path', "")
						break
			return path

		def config_set_current(self, path: str) -> None:
			parser = configparser.ConfigParser()
			parser.read(configOptions.dict_from_parser()['PATHS']['config_file'])
			parser.set('DATA_SET', 'current', path)
			config_file: file = open(configOptions.dict_from_parser()['PATHS']['config_file'], 'w')
			parser.write(config_file)
			config_file.close()
			return None


		def change_current(self, new_current: str) -> None:
			#change .config
			path: str = self.get_path(new_current)	
			self.config_set_current(path)
			#change data_sets
			py_dict: dict = self.json_handler.get_json(self.dss_paths)
			for key in list(py_dict):
				for key2 in list(py_dict[key]):
					if py_dict[key][key2].get('alias', "") == new_current:
					 	py_dict[key][key2]['current'] = True
					else:
						py_dict[key][key2]['current'] = False
			self.json_handler.dump_json(self.dss_paths, py_dict)
			print("'" + new_current + "' is the new current data set")
			return None
		
	def __init__(self):
		self.dss_paths: str = configOptions.dict_from_parser()['PATHS']['data_sets_file']
		self.dss_dir_path: str = configOptions.dict_from_parser()['PATHS']['data_sets_dir']
		self.all_dss: dict = JsonHandler().get_json(self.dss_paths)
		self.data_set_inner = self.__DataSetInner(self.dss_paths, self.all_dss)


	def add_new(self, given_name: str):
		"""Adds a new data set and sets it to be current"""

		alias: str = given_name
		py_dict: dict = self.all_dss
		i: int = 0
		for key in list(py_dict):
			for key2 in list(py_dict[key]):
				i += 1
				if py_dict[key][key2].get('current', False):
					 py_dict[key][key2]['current'] = False

		py_dict['data_sets']['data_set_' + str(i + 1)] = {
						'alias': alias,
						'current': True,
						'path': self.dss_dir_path + "dataSet" + str(i + 1) + ".json"
		}
		
		JsonHandler().dump_json(self.dss_paths, py_dict)
		new_data_file: file = open(py_dict['data_sets']['data_set_' + str(i + 1)]['path'], 'w')
		new_data_file.close()
		self.data_set_inner.config_set_current(py_dict['data_sets']['data_set_' + str(i + 1)]['path'])
		print(alias + " was created and is now the new current data set")

		
	def change_current(self, given_name: str) -> None:
		"""Just changes the current"""
		aliases: list = self.data_set_inner.get_existing_aliases()
		if given_name in aliases:
			self.data_set_inner.change_current(given_name)
		else:
			print("No {} found".format(given_name))
		return None
					
	def show_current(self) -> None:
		"""Just shows the current"""
		for key in self.all_dss:
			for key2 in self.all_dss[key]:
				if self.all_dss[key][key2].get('current', False):
					print("Current data set: " + self.all_dss[key][key2].get('alias', "Not Found"))
					return None

	def list_existing(self) -> None:
		"""Lits all created data sets"""
		path: str = configOptions.dict_from_parser()['PATHS']['data_sets_file']
		if os.stat(path).st_size == 0:
			print("There are no data sets")
		else:
			py_dict: dict = JsonHandler().get_json(path)
			aliases: list = []
			for key in py_dict:
				for key2 in py_dict[key]:
					aliases.append(py_dict[key][key2].get('alias'))
			for i in range(0, len(aliases), 1):
				print(str(i) + ": " + aliases[i]) 
		return None

	def delete(self, aliases: list) -> None:
		"""Deletes a data set"""

		file_path: str = ""
		
		for alias in aliases.copy():
			for key in list(self.all_dss):
				for key2 in list(self.all_dss[key]):
					if alias == "Default":
						self.wipe(["Default"])
						aliases.remove("Default")
						print("'Default' is never deleted, only cleaned")
					elif alias == self.all_dss[key][key2].get('alias', ""):
						file_path = self.all_dss[key][key2]['path']
						os.remove(file_path)
						if self.all_dss[key][key2].get('current', False): 
							self.data_set_inner.change_current('Default')
						new_set_dict: dict = JsonHandler().get_json(self.dss_paths)
						del new_set_dict[key][key2]
						JsonHandler().dump_json(self.dss_paths, new_set_dict)
						print(alias + " deleted")
						aliases.remove(alias)
		if aliases:
			for elem in aliases:
				print("{} not found".format(alias))
		return None

	def wipe(self, aliases: list) -> None:
		"""Remove all entries from a data set by truncating it with '0' as an argument"""
		for alias in aliases.copy():
			for key in self.all_dss:
				for key2 in self.all_dss[key]:
					if self.all_dss[key][key2].get('alias', "") == alias:	
						with open(self.all_dss[key][key2]['path'], 'w') as data_set:
							data_set.truncate(0)
							print("{} cleaned".format(alias))
							aliases.remove(alias)
		if aliases:
			for elem in aliases:
				print("{} not found".format(elem))
		return None

##########################################################################################################################
