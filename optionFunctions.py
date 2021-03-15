#!/usr/bin/python3

import os, sys, json, configparser, fnmatch, enum, datetime
import configOptions
from cryptonator import get_available_currencies, get_exchange_rate
from  yahooquery import Ticker
from subFunctions import dataSet 


class JsonHandler:
	"""Simple class that handles getting a dict from a .json and outputting a dict to a .json """

	def get_json(self, path: str) -> dict:
		"""Returns a dict from a .json"""

		r_file: file = open(path, 'r')
		py_dict: dict = json.load(r_file)
		r_file.close()
		return py_dict
		

	def dump_json(self, path: str, py_dict: dict, indentation: int=2):
		"""Outputs a .json"""

		w_file: file = open(path, 'w')
		json.dump(py_dict, w_file, indent=indentation)
##########################################################################################################################
class Entry:
	"""Class responsible for adding, listing and removing entries"""

	def __init__(self, jh=JsonHandler()):
		self.json_handler = jh
	
########Adding Entries####################################################################################################
	class DICT_MODES(enum.Enum):
		OLD = 0
		NEW = 1
		BRAND_NEW = 2

	def new_dict(self, mode: int, price: float, quantity: float, ticker: str="") -> dict:
		"""Returns a dict to an empty .json (DICT_MODES.BRAND_NEW) and to non empty ones by adding either a new
		key (DICT_MODES.NEW and ticker != "") or appending to an existing one (DICT_MODES.OLD and ticker = "")"""

		c_dict: dict = {}
	
		if mode == self.DICT_MODES.OLD:
			c_dict = {
				"price": price,
				"quantity": quantity,
				"date": str(datetime.date.today())
			}
	
		elif mode == self.DICT_MODES.NEW:
			c_dict = { 
				"entry_1": {
					"price": price,
					"quantity": quantity,
					"date": str(datetime.date.today())
				}
			}
		
		elif mode == self.DICT_MODES.BRAND_NEW:
			c_dict = {
				ticker: { 
					"entry_1": {
						"price": price,
						"quantity": quantity,
						"date": str(datetime.date.today())
					}
				}
			}
		
		return c_dict


	def add_new(self, ticker: str, mode: int=DICT_MODES.NEW) -> None:
		"""Void private function that outputs to either an empty (DICT_MODES.BRAND_NEW) or
		to a non empty (DICT_MODES.NEW) .json"""

		price: float = float(input("Enter the price of the asset: "))
		quantity: float = float(input("Enter the quantity of the asset: "))
		path: str = configOptions.dict_from_parser()['DATA_SET']['current']

		if mode == self.DICT_MODES.NEW:
			new_entry: dict = self.new_dict(mode, price, quantity)
			old_entry: dict = self.json_handler.get_json(path)	
			old_entry[ticker] = new_entry
			self.json_handler.dump_json(path, old_entry)
	
		elif mode == self.DICT_MODES.BRAND_NEW:
			new_entry: dict = self.new_dict(mode, price, quantity, ticker)
			self.json_handler.dump_json(path, new_entry)

	def add_to_old(self, ticker: str) -> None:
		"""Void private function that outputs to an non empty .json that already has the key (ticker)"""

		price: float = float(input("Enter the price of the asset: "))
		quantity: float = float(input("Enter the quantity of the asset: "))
		path: str = configOptions.dict_from_parser()['DATA_SET']['current']
		old_entry: dict = self.json_handler.get_json(path)
		
		i: int = 0 
		for key in old_entry[ticker]:
			if 'entry_' in key:
				i += 1
	
		old_entry[ticker]['entry_' + str(i + 1)] = self.new_dict(self.DICT_MODES.OLD, price, quantity)
	
		self.json_handler.dump_json(path, old_entry)
	

	def add_entry(self):
		"""Adds a new entry to the current data set by defining if the output .json is either 
		empty (DICT_MODES.BRAND_NEW), not empty, but without the given key (ticker), or not empty
		with the given key.

		Then it selects between add_to_old(self, ticker: str) and add_new(self, ticker: str,
		mode: int=DICT_MODES.NEW)"""

		ticker: str = input("Enter asset name: ")
		path: str = configOptions.dict_from_parser()['DATA_SET']['current']
		if os.stat(path).st_size == 0:
			self.add_new(ticker, self.DICT_MODES.BRAND_NEW)
		else:
			py_dict: dict = self.json_handler.get_json(path)
		
			for key in py_dict:
				if key == ticker:
					self.add_to_old(ticker)
					return None
			
			self.add_new(ticker)
########Listing entries###################################################################################################
	def table_mode(self, tickers: list) -> None:
		"""This functions is responsible for fetching the price of assests and for displaying the latter"""

		def get_non_crypto(ticker, base_currency):
			"""This functions uses the 'yahooquery' module, when 'ticker' is not in 
			get_available_currencies()"""

			asset: Ticker = Ticker(ticker)
			#Appends '.sa' if the stock is brazillian
			if "Quote not found for ticker symbol: {}".format(ticker.upper()) in asset.price[ticker]:
				ticker += ".sa"
				asset = Ticker(ticker)		
	
			given_currency: str = asset.price[ticker].get('currency', "")
			if given_currency != base_currency:
				asset_price: float = 0.0  if given_currency not in get_available_currencies() \
				else get_exchange_rate(given_currency.lower(), currency.lower()) * \
				asset.price[ticker].get('regularMarketPrice', 0.0)
			else:
				asset_price: float = asset.price[ticker].get('regularMarketPrice', 0.0)
	
			return asset_price


		path: str = configOptions.dict_from_parser()['DATA_SET']['current']
		py_dict: dict = self.json_handler.get_json(path)
		found: bool = True
		not_found_list: list = []
		currency: str = configOptions.dict_from_parser()['SETUP']['base_currency']
		grapheme: str = "$" if currency not in self.json_handler.get_json("currency-format.json") \
		else self.json_handler.get_json("currency-format.json")[currency]['symbol'].get('grapheme', "$")
	
		if tickers:
			found = False
			for ticker in tickers:
				if ticker not in py_dict:
					not_found_list.append(ticker)
				else:
					found = True
		if found:
			print("{:.<15}{:.<15}{:.<15}Value".format("Ticker","Quantity", "Price"))

		for ticker in py_dict:
			if tickers and ticker not in tickers:
				continue 
			qtd: float = 0.0
			price: float = float(get_non_crypto(ticker, currency)) \
	 		if ticker not in get_available_currencies() \
			else get_exchange_rate(ticker.lower(), currency.lower())
			value: float = 0.0
			for key in py_dict[ticker]:
				qtd += py_dict[ticker][key].get('quantity', 0.0)
			value = qtd * price
			print("{:<15}{:<15}{:<15}".format(ticker, str(qtd), "{} ".format(grapheme) + "%.2f" %  price) \
			+ "{} ".format(grapheme) + "%.2f" % value)
	
		if not_found_list:
			print("")
			for ticker in not_found_list:
				print(ticker + " not found")

	def json_mode(self, tickers: list):
		"""Prints the complete data set in json format"""

		path: str = configOptions.dict_from_parser()['DATA_SET']['current']
		py_dict: dict = self.json_handler.get_json(path)
		not_found_list: list = []
		print(json.dumps(py_dict, indent=2, sort_keys=True))

	def list_entries(self):
		"""Lists the entries of the current data set as a table (table_mode()) or as the other supported
		formats:
		1) json(json_mode())"""
		path: str = configOptions.dict_from_parser()['DATA_SET']['current']
		args: list = [] if len(sys.argv) < 3 \
		else [foo for foo in sys.argv[2:] if not fnmatch.fnmatch(foo, 'as=?*')]
		possible_modes: list = fnmatch.filter(sys.argv, 'as=?*')
	
		def switch_list(option: str, tickers: list):
			cases: dict = {
				'json': self.json_mode
			}
			cases.get(option, self.table_mode)(tickers)
	
		if os.stat(path).st_size == 0:
			print("There are no entries in the data file")
		else:
			mode: str = possible_modes.pop(-1)[3:] if len(possible_modes) > 0 else ""
			switch_list(mode, args)
##########################################################################################################################


def data_base():
	data_sets_paths: str = configOptions.dict_from_parser()['PATHS']['data_sets_file']
	data_sets_dir: str = configOptions.dict_from_parser()['PATHS']['data_sets_dir']
	all_data_sets: dict = JsonHandler().get_json(data_sets_paths)
	
	
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
		
		JsonHandler().dump_json(data_sets_paths, py_dict)
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
		py_dict: dict = JsonHandler().get_json(path)
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
	all_data_sets: dict = JsonHandler().get_json(data_sets_paths)
	
	if alias == "Default":
		clean_data_base()
		print("'Default' is never deleted, only cleaned")
	else:
		for key in list(all_data_sets):
			for key2 in list(all_data_sets[key]):
				if alias == all_data_sets[key][key2].get('alias', ""):
					file_path = all_data_sets[key][key2]['path']
					os.remove(file_path)
					if all_data_sets[key][key2].get('current', False): 
						dataSet.change_current('Default')
					new_set_dict: dict = JsonHandler().get_json(data_sets_paths)
					del new_set_dict[key][key2]
					JsonHandler().dump_json(data_sets_paths, new_set_dict)
					print(alias + " deleted")
					return None
						
		print("'" + alias + "' not found")

def clean_data_base():
	data_sets_file_path: str = configOptions.dict_from_parser()['PATHS']['data_sets_file']
	data_sets_dict: dict = JsonHandler().get_json(data_sets_file_path)
	
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

