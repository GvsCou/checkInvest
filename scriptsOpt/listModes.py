import sys, json
import configOptions, cryptonator
from . import entry

def table_mode(tickers: list):
	path: str = configOptions.dict_from_parser()['DATA_SET']['current']
	py_dict: dict = entry.get_json(path)
	found: bool = True
	not_found_list: list = []
	currency: str = configOptions.dict_from_parser()['SETUP']['base_currency']
	grapheme: str = "$" if currency not in entry.get_json("currency-format.json") \
	else entry.get_json("currency-format.json")[currency]['symbol'].get('grapheme', "$")
	print(grapheme)
	exit()
	
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
		price: float = 0.0 if ticker not in cryptonator.get_available_currencies() \
		else cryptonator.get_exchange_rate(ticker.lower(), currency.lower())
		value: float = 0.0
		for key in py_dict[ticker]:
			qtd += py_dict[ticker][key].get('quantity', 0.0)
		value = qtd * price
		print("{:<15}{:<15}{:<15}".format(ticker, str(qtd), "U$ %.2f" % price) + "U$ %.2f" % value)
		#print(ticker + '\t' + str(qtd) + '\t' + "%.2f" % price + '\t' + "%.2f" % value)
	
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
