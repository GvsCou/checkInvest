#!/usr/bin/python3

import json
import os
import datetime
import enum
from paths import paths

class DICT_MODES(enum.Enum):
	OLD = 0
	NEW = 1

def new_dict(mode: int, price: float, quantity: float, ticker: str="") -> dict:
	c_dict: dict = {}

	if mode == DICT_MODES.NEW:
		c_dict = { 
			ticker: {
				"entry_1": {
					"price": price,
					"quantity": quantity,
					"date": str(datetime.date.today())
				}
			}
		}

	elif mode == DICT_MODES.OLD:
		c_dict = {
			"price": price,
			"quantity": quantity,
			"date": str(datetime.date.today())
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


def add_new(ticker: str):
	price: float = float(input("Enter the price of the asset: "))
	quantity: float = float(input("Enter the quantity of the asset: "))
	
	new_entry: dict = new_dict(DICT_MODES.NEW, price, quantity, ticker)
	
	dump_json(paths['data_file'], new_entry)


def add_to_old(ticker: str):
	price: float = float(input("Enter the price of the asset: "))
	quantity: float = float(input("Enter the quantity of the asset: "))
	
	old_entry: dict = get_json(paths['data_file'])
	
	i: int = 1 
	for key in old_entry[ticker]:
		if key == 'entry_?':
			++i
	
	old_entry[ticker]['entry_' + str(i + 1)] = new_dict(DICT_MODES.OLD, price, quantity)

	dump_json(paths['data_file'], old_entry)
