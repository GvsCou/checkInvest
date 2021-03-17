#!/usr/bin/python3

import os, sys, json, configparser, fnmatch, enum, datetime
import configOptions
from cryptonator import get_available_currencies, get_exchange_rate
from yahooquery import Ticker


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


	def add_new(self, ticker: str, price: float, quantity: float, mode: int=DICT_MODES.NEW) -> None:
		"""Void private function that outputs to either an empty (DICT_MODES.BRAND_NEW) or
		to a non empty (DICT_MODES.NEW) .json"""

		path: str = configOptions.dict_from_parser()['DATA_SET']['current']

		if mode == self.DICT_MODES.NEW:
			new_entry: dict = self.new_dict(mode, price, quantity)
			old_entry: dict = self.json_handler.get_json(path)	
			old_entry[ticker] = new_entry
			self.json_handler.dump_json(path, old_entry)
	
		elif mode == self.DICT_MODES.BRAND_NEW:
			new_entry: dict = self.new_dict(mode, price, quantity, ticker)
			self.json_handler.dump_json(path, new_entry)
		print(ticker + " entry added")

	def add_to_old(self, ticker: str, price: float, quantity: float) -> None:
		"""Void private function that outputs to an non empty .json that already has the key (ticker)"""

		path: str = configOptions.dict_from_parser()['DATA_SET']['current']
		old_entry: dict = self.json_handler.get_json(path)
		
		i: int = 0 
		for key in old_entry[ticker]:
			if 'entry_' in key:
				i += 1
	
		old_entry[ticker]['entry_' + str(i + 1)] = self.new_dict(self.DICT_MODES.OLD, price, quantity)
	
		self.json_handler.dump_json(path, old_entry)
		print(ticker + " entry added")
	

	def add_entry(self, data: list=[], is_interactive: bool=False):
		"""Adds a new entry to the current data set by defining if the output .json is either 
		empty (DICT_MODES.BRAND_NEW), not empty, but without the given key (ticker), or not empty
		with the given key.

		Then it selects between add_to_old(self, ticker: str) and add_new(self, ticker: str,
		mode: int=DICT_MODES.NEW)"""

		if is_interactive:
			ticker: str = input("Enter the asset name: ").upper()
			price: float = float(input("Enter the asset's price: ").replace(",","."))
			quantity: float = float(input("Enter the asset's quantity: ").replace(",","."))
		elif len(data) < 3:
			print("In non-interactive mode, you must enter these arguments in the following order:")
			exit()
		else:
			ticker: str = data[0].upper()
			price: float = float(data[1].replace(",","."))
			quantity: float = float(data[2].replace(",","."))
		path: str = configOptions.dict_from_parser()['DATA_SET']['current']
		if os.stat(path).st_size == 0:
			self.add_new(ticker, price, quantity, self.DICT_MODES.BRAND_NEW)
		else:
			py_dict: dict = self.json_handler.get_json(path)
		
			for key in py_dict:
				if key == ticker:
					self.add_to_old(ticker, price, quantity)
					return None
			
			self.add_new(ticker, price, quantity)
			

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
			print(asset.price[ticker])	
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


	def add_new(self):
		"""Adds a new data set and sets it to be current"""
		if len(sys.argv) < 3:
			print("No alias given")
			return None
		alias: str = sys.argv[2:].pop(-1)
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

		
	def change_current(self) -> None:
		"""Just changes the current"""
		if len(sys.argv) > 2:
			aliases: list = self.data_set_inner.get_existing_aliases()
			args: list = sys.argv
			del args[0:2]
			for arg in args:
				if arg in aliases:
					self.data_set_inner.change_current(arg)
					return None
				else:
					print("No {} found".format(arg))
		else:
			print("No alias given")
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

	def remove(self) -> None:
		"""Deletes a data set"""
		if len (sys.argv) < 3:
			print("No data set given")
			return None
		alias: str = sys.argv[2]
		file_path: str = ""
		
		if alias == "Default":
			self.clean()
			print("'Default' is never deleted, only cleaned")
		else:
			for key in list(self.all_dss):
				for key2 in list(self.all_dss[key]):
					if alias == self.all_dss[key][key2].get('alias', ""):
						file_path = self.all_dss[key][key2]['path']
						os.remove(file_path)
						if self.all_dss[key][key2].get('current', False): 
							self.data_set_inner.change_current('Default')
						new_set_dict: dict = JsonHandler().get_json(self.dss_paths)
						del new_set_dict[key][key2]
						JsonHandler().dump_json(self.dss_paths, new_set_dict)
						print(alias + " deleted")
						return None
							
			print("'" + alias + "' not found")
		return None

	def clean(self) -> None:
		"""Remove all entries from a data set by truncating it with '0' as an argument"""
		if len(sys.argv) < 3:
			print("No data set specified")
		else:
			for alias in sys.argv[2:]:
				for key in self.all_dss:
					for key2 in self.all_dss[key]:
						if self.all_dss[key][key2].get('alias', "") == alias:	
							data_set: file = open(self.all_dss[key][key2]['path'], 'w')
							data_set.truncate(0)
							data_set.close()
			print("{} cleaned".format(alias))
		return None

##########################################################################################################################

def default():
	print("Invalid Option")

