#!/usr/bin/python3

import getpass, os

config_dir: str = '/home/' + getpass.getuser() + '/.config/checkInvest/'

config_file_dict: dict = {
        'path': config_dir + 'checkInvest.config'
}

data_file_dict: dict = {
        'path': config_dir + 'data.json'
}

def check_base_files():
    if os.path.isfile(config_file_dict['path']) and os.path.isfile(data_file_dict['path']):
            pass
    else:
        if not os.path.isdir(config_dir):
            os.mkdir(config_dir)
        if not os.path.isfile(config_file_dict['path']):
            config_file_dict['file'] = open(config_file_dict['path'],'w')
            config_file_dict['file'].close()
        if not os.path.isfile(data_file_dict['path']):
            data_file_dict['file'] = open(data_file_dict['path'], 'w')
            data_file_dict['file'].close()

check_base_files()
