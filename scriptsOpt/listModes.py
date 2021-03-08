import sys, json
import setup
from . import entry

def table_mode(tickers: list):
	path: str = setup.dict_from_parser()['DATA_SET']['current']
	py_dict: dict = entry.get_json(path)
	found: bool = True
	
	if tickers:
		found = False
		for ticker in tickers:
			if ticker not in py_dict:
				print(ticker + " not Found")
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
		

def json_mode(tickers: list):
	path: str = setup.dict_from_parser()['DATA_SET']['current']
	py_dict: dict = entry.get_json(path)
	print(json.dumps(py_dict, indent=2, sort_keys=True))
