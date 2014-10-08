#!/usr/bin/python3

import json
from collections import OrderedDict

__json_path = None
__json_data = None
__sorted = None

debug = False
def trace(function):
    def wrapper(*args, **kwargs):
        if debug:
            print("{function_name}({arguments}{comma}{keywords})".format(
                    function_name = function.__name__,
                    arguments = ", ".join([repr(arg) for arg in args]),
                    comma = ", " if len(args) and len(kwargs) else "",
                    keywords = ", ".join(["{}={!r}".format(key, kwargs[key]) for key in kwargs])))
        return function(*args, **kwargs)
    return wrapper

@trace
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

@trace
def keys_at(path=None):
    data = json_at(path)
    if not isinstance(data, OrderedDict):
        return {}

    type_mappings = {
        "<class 'collections.OrderedDict'>": "object",
        "<class 'bool'>": "boolean",
        "<class 'str'>": "string",
        "<class 'int'>": "number",
        "<class 'float'>": "number"
    }
    return {key: type_mappings[str(type(data[key]))] for key in data.keys()}

@trace
def save(file_path):
    global __json_path
    global __json_data

    if file_path:
        __json_path = file_path
    with open(__json_path, "w") as json_file:
        json_file.write(to_string())

@trace
def set_property(path, value):
    path_parts = path.rpartition(".")
    data = json_at(path_parts[0])

    # I suppose this is how you try-parse in Python.
    try:
        value = json.loads(value)
    except ValueError:
       pass 

    print(repr(value))
    print("Type:", type(value))

    data[path_parts[2]] = value

@trace
def remove_property(path):
    path_parts = path.rpartition(".")
    data = json_at(path_parts[0])
    del data[path_parts[2]]

@trace
def json_at(path=None):
    data = __json_data
    if path:
        for prop in path.split("."):
            data = data[prop]

    return data
