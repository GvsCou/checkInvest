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

def add_new():
	ticker: str = input("Enter the name of the asset: ")
	price: float = float(input("Enter the price of the asset: "))
	quantity: float = float(input("Enter the quantity of the asset: "))
	new_entry: dict = new_dict(DICT_MODES.NEW, price, quantity, ticker)
	
	out_file = open(paths['data_file'], 'w')
	json.dump(new_entry, out_file, indent = 2)
	out_file.close()

def add_to_old():
	ticker: str = input("Enter the name of the asset: ")
	price: float = float(input("Enter the price of the asset: "))
	quantity: float = float(input("Enter the quantity of the asset: "))
	
	out_file = open(paths['data_file'], 'r')
	old_entry: dict = json.load(out_file)
	out_file.close()
	
	i: int = 1 
	for key in old_entry[ticker]:
		if key == 'entry_?':
			++i
	
	old_entry[ticker]['entry_' + str(i + 1)] = new_dict(DICT_MODES.OLD, price, quantity)

	out_file = open(paths['data_file'], 'w')
	json.dump(old_entry, out_file, indent = 2)
	out_file.close()

