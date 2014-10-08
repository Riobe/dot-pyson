#!/usr/bin/python3

import json
from collections import OrderedDict

__json_path = None
__json_data = None
__sorted = None

def load(file_path, load_sorted):
    global __json_data
    global __json_path
    global __sorted

    __sorted = load_sorted
    __json_path = file_path

    with open(__json_path) as json_file:
        if __sorted:
            unsorted_data = json.load(json_file)
            __json_data = json.loads(json.dumps(unsorted_data, sort_keys=True), object_pairs_hook = OrderedDict)
        else:
            __json_data = json.load(json_file, object_pairs_hook = OrderedDict)
            
def to_string(path=None):
    return json.dumps(json_at(path), sort_keys=__sorted, indent=4, separators=(",", ": "))

def keys_at(path=None):
    return json_at(path).keys()

def save(file_path):
    global __json_path
    global __json_data

    if file_path:
        __json_path = file_path
    with open(__json_path, "w") as json_file:
        json_file.write(to_string())

def set_property(path, value):
    path_parts = path.rpartition(".")
    data = json_at(path_parts[0])
    data[path_parts[2]] = value

def remove_property(path):
    path_parts = path.rpartition(".")
    data = json_at(path_parts[0])
    del data[path_parts[2]]

def json_at(path=None):
    data = __json_data
    if path:
        for prop in path.split("."):
            data = data[prop]

    return data
