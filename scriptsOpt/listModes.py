import sys, json
import setup
from . import entry

def table_mode(do_all: bool, tickers: list):
	path: str = setup.dict_from_parser()['DATA_SET']['current']
	py_dict: dict = entry.get_json(path)
	
	print("Ticker" + '\t' + "Quantity")
	for ticker in py_dict:
		qtd: float = 0.0
		for key in py_dict[ticker]:
			qtd += py_dict[ticker][key].get('quantity', 0.0)
		print(ticker + '\t' + str(qtd))

def json_mode(do_all: bool, tickers: list):
	path: str = setup.dict_from_parser()['DATA_SET']['current']
	py_dict: dict = entry.get_json(path)
	print(json.dumps(py_dict, indent=2, sort_keys=True))
