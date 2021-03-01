#!/usr/bin/python3

import enum, os, json, datetime
import setup

class DICT_MODES(enum.Enum):
	OLD = 0
	NEW = 1
	BRAND_NEW = 2


def new_dict(mode: int, price: float, quantity: float, ticker: str="") -> dict:
	c_dict: dict = {}

	if mode == DICT_MODES.OLD:
		c_dict = {
			"price": price,
			"quantity": quantity,
			"date": str(datetime.date.today())
		}

	elif mode == DICT_MODES.NEW:
		c_dict = { 
			"entry_1": {
				"price": price,
				"quantity": quantity,
				"date": str(datetime.date.today())
			}
		}
	
	elif mode == DICT_MODES.BRAND_NEW:
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


def get_json(path: str) -> dict:
	r_file: file = open(path, 'r')
	py_dict: dict = json.load(r_file)
	r_file.close()
	return py_dict
		

def dump_json(path: str, py_dict: dict, indentation: int=2):
	w_file: file = open(path, 'w')
	json.dump(py_dict, w_file, indent=indentation)


def add_new(ticker: str, mode: int=DICT_MODES.NEW):
	price: float = float(input("Enter the price of the asset: "))
	quantity: float = float(input("Enter the quantity of the asset: "))
	path: str = setup.dict_from_parser()['PATHS']['data_file']
	
	if mode == DICT_MODES.NEW:
		new_entry: dict = new_dict(mode, price, quantity)
		old_entry: dict = get_json(path)	
		old_entry[ticker] = new_entry
		dump_json(path, old_entry)

	elif mode == DICT_MODES.BRAND_NEW:
		new_entry: dict = new_dict(mode, price, quantity, ticker)
		dump_json(path, new_entry)

def add_to_old(ticker: str):
	price: float = float(input("Enter the price of the asset: "))
	quantity: float = float(input("Enter the quantity of the asset: "))
	path: str = setup.dict_from_parser()['PATHS']['data_file']
	old_entry: dict = get_json(path)
	
	i: int = 0 
	for key in old_entry[ticker]:
		if 'entry_' in key:
			i += 1

	old_entry[ticker]['entry_' + str(i + 1)] = new_dict(DICT_MODES.OLD, price, quantity)

	dump_json(path, old_entry)
