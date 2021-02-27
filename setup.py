#!/usr/bin/python3

import getpass, os

config_dir: str = '/home/' + getpass.getuser() + '/.config/checkInvest/'

config_file_dict: dict = {
        'path': config_dir + 'checkInvest.config'
}

def check_config():
    if os.path.isfile(config_file_dict['path']):
            pass
    else:
        if not os.path.isdir(config_dir):
            os.mkdir(config_dir)
        if not os.path.isfile(config_file_dict['path']):
            config_file_dict['file'] = open(config_file_dict['path'],'w')
            config_file_dict['file'].close()

check_config()
