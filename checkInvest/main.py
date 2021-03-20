#!/usr/bin/python3

from .optionFunctions import ArgHandler
from .configOptions import check_base_files

def main():
	check_base_files()
	ArgHandler().handle()

if __name__=='__main__':
	main()
