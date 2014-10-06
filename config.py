#!/usr/bin/python3

import json
from pprint import pprint

json_path = None
json_data = None

def load(file_path):
    global json_data
    global json_path

    json_path = file_path
    with open(json_path) as json_file:
        json_data = json.load(json_file)

def debug():
    for line in json_file.readlines():
        print(line)
    load(json_path)

def view():
    print(json.dumps(json_data, sort_keys=True, indent=4, separators=(',', ': ')))

def close():
    close(json_file)

