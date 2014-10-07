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

def to_string():
    return json.dumps(__json_data, sort_keys=True, indent=4, separators=(',', ': '))

def keys_at(path):
    data = __json_data[path] if path else __json_data
    return data.keys()

