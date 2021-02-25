#!/usr/bin/python3

import json
import os
import datetime

def new_dict_entry(ticker: str, entry: str, price: float, quantity: float) -> dict:
    new_entry: dict = {
            ticker: {
                entry: {
                    "price": price,
                    "quantity": quantity,
                    "date": str(datetime.date.today())
                }
            }
    }
    return new_entry

def add_new():
    ticker: str = input("Enter the name of the asset: ")
    price: float = float(input("Enter the price of the asset: "))
    quantity: float = float(input("Enter the quantity of the asset: "))

    if not os.path.isdir('entries'):
        os.mkdir('entries')

    new_entry: dict = new_dict_entry(ticker, "entry_1", price, quantity)

    out_file = open('entries/' + ticker + '.json', 'w')
    json.dump(new_entry, out_file, indent = 2)
    out_file.close()

def old_dict_entry(price: float, quantity: float) -> dict:
    old_entry: dict = {        
        "price": price,
        "quantity": quantity,
        "date": str(datetime.date.today())
    }
    return old_entry

def add_to_old():
    ticker: str = input("Enter the name of the asset: ")
    price: float = float(input("Enter the price of the asset: "))
    quantity: float = float(input("Enter the quantity of the asset: "))

    out_file = open('entries/' + ticker + '.json', 'r')
    old_entry: dict = json.load(out_file)
    out_file.close()

    i: int = 1 
    for key in old_entry[ticker]:
        if key == 'entry_?':
            ++i
    
    old_entry[ticker]['entry_' + str(i + 1)] = old_dict_entry(price, quantity)

    out_file = open('entries/' + ticker + '.json', 'w')
    json.dump(old_entry, out_file, indent = 2)
    out_file.close()

