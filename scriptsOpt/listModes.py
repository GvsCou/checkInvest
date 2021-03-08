import sys, json
import setup
from . import entry

def table_mode(tickers: list):
	path: str = setup.dict_from_parser()['DATA_SET']['current']
	py_dict: dict = entry.get_json(path)
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
		print("Ticker" + '\t' + "Quantity")

	for ticker in py_dict:
		if tickers and ticker not in tickers:
			continue 
		qtd: float = 0.0
		for key in py_dict[ticker]:
			qtd += py_dict[ticker][key].get('quantity', 0.0)
		print(ticker + '\t' + str(qtd))
	
	if not_found_list:
		print("")
		for ticker in not_found_list:
			print(ticker + " not found")
		

def json_mode(tickers: list):
	path: str = setup.dict_from_parser()['DATA_SET']['current']
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
