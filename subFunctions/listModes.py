import sys, json
import configOptions, cryptonator
from yahooquery import Ticker
from . import entry

def table_mode(tickers: list) -> str:
	def get_non_crypto(ticker, base_currency):
		asset: Ticker = Ticker(ticker)
		#Appends '.sa' if the stock is brazillian
		if "Quote not found for ticker symbol: {}".format(ticker.upper()) in asset.price[ticker]:
			ticker += ".sa"
			asset = Ticker(ticker)		

		given_currency: str = asset.price[ticker].get('currency', "")
		if given_currency != base_currency:
			asset_price: float = 0.0  if given_currency not in cryptonator.get_available_currencies() \
			else cryptonator.get_exchange_rate(given_currency.lower(), currency.lower()) * \
			asset.price[ticker].get('regularMarketPrice', 0.0)
		else:
			asset_price: float = asset.price[ticker].get('regularMarketPrice', 0.0)

		return asset_price


	path: str = configOptions.dict_from_parser()['DATA_SET']['current']
	py_dict: dict = entry.get_json(path)
	found: bool = True
	not_found_list: list = []
	currency: str = configOptions.dict_from_parser()['SETUP']['base_currency']
	grapheme: str = "$" if currency not in entry.get_json("currency-format.json") \
	else entry.get_json("currency-format.json")[currency]['symbol'].get('grapheme', "$")
	
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
	 	if ticker not in cryptonator.get_available_currencies() \
		else cryptonator.get_exchange_rate(ticker.lower(), currency.lower())
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
		

def json_mode(tickers: list):
	path: str = configOptions.dict_from_parser()['DATA_SET']['current']
	py_dict: dict = entry.get_json(path)
	not_found_list: list = []

	if not tickers:
		print(json.dumps(py_dict, indent=2, sort_keys=True))
	else:
		if tickers:
			for ticker in tickers:
				if ticker not in py_dict:
					not_found_list.append(ticker)

		for ticker in py_dict:
			if tickers and ticker not in tickers:
				continue 
			print("Entries for " + ticker)
			print(json.dumps(py_dict[ticker], indent=2, sort_keys=True))		

		if not_found_list:
			for ticker in not_found_list:
				print(ticker + " not found")
