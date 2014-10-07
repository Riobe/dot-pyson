#!/usr/bin/python3

import json
from collections import OrderedDict

__json_path = None
__json_data = None

def load(file_path, load_sorted):
    global __json_data
    global __json_path

    __json_path = file_path
    with open(__json_path) as json_file:
        if load_sorted:
            unsorted_data = json.load(json_file)
            __json_data = json.loads(json.dumps(unsorted_data, sort_keys=True), object_pairs_hook = OrderedDict)
        else:
            __json_data = json.load(json_file, object_pairs_hook = OrderedDict)
            
def to_string(path=None):
    data = __json_data[path] if path else __json_data
    return json.dumps(data, indent=4, separators=(',', ': '))

def keys_at(path):
    data = __json_data[path] if path else __json_data
    return data.keys()

def save(file_path):
    global __json_path
    global __json_data

    if file_path:
        __json_path = file_path
    with open(__json_path, 'w') as json_file:
        json_file.write(to_string())

