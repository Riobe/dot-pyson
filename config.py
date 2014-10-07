#!/usr/bin/python3

import json
from pprint import pprint

__json_path = None
__json_data = None

def load(file_path):
    global __json_data
    global __json_path

    __json_path = file_path
    with open(__json_path) as json_file:
        __json_data = json.load(json_file)

def view():
    print(json.dumps(__json_data, sort_keys=True, indent=4, separators=(',', ': ')))

