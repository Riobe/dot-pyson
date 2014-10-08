#!/usr/bin/python3

import sys
import os
import readline
import glob
import shlex

from config import trace
import config

__command_actions = {}
__file_actions = []
__key_actions = []
__prompt = ">>>"
__sort = True
__last_viewed = ""
__time_to_go = False

def command(name):
    def command_decorator(function):
        __command_actions[name] = function
        return function
    return command_decorator

def file_command(name):
    def command_decorator(function):
        __command_actions[name] = function
        __file_actions.append(name)
        return function
    return command_decorator

def key_command(name):
    def command_decorator(function):
        __command_actions[name] = function
        __key_actions.append(name)
        return function
    return command_decorator


def main():
    global __prompt
    global __time_to_go

    print("JSON configuration utility version (1.0.0)")
    handle_arguments()

    readline.set_completer_delims("\t\n")
    readline.parse_and_bind("tab: complete")
    readline.set_completer(auto_complete)

    command = ""
    while True:
        try:
            user_input = input(__prompt + " ").strip()
        except KeyboardInterrupt:
            print()
            if __time_to_go:
                exit_command()
            else:
                __time_to_go = True
                print("Press ^C again to close. Running another command resets this.")
                continue

        if not user_input:
            continue

        run_command(user_input)
        __time_to_go = False

@trace
def auto_complete(text, state):
    for command in __file_actions:
        command += " "
        if text.startswith(command):
            return ([command + path for path in glob.glob(text.replace(command, "")+"*")]+[None])[state]

    for command in __key_actions:
        command += " "
        if text.startswith(command):
            key_info = text.partition(" ")[2].rpartition(".")
            return ([command + key_info[0] + key_info[1] + key
                        for key 
                        in config.keys_at(key_info[0]) 
                        if key.startswith(key_info[2])]+[None])[state]

    return ([command for command in __command_actions.keys() if command.startswith(text)]+[None])[state]

@trace
def run_command(command_line):
        command_line = command_line.split(" ")
        command = command_line[0]
        arguments = shlex.split(" ".join(command_line[1:]))

        if command in __command_actions:
            try:
                __command_actions[command](*arguments)
            except TypeError as error:
                print("An incorrect number of arguments were supplied.")
                help_command(command)
        else:
            print("Unrecognized command")

@trace
def handle_arguments():
    global __prompt
    global __sort

    # No arguments.
    if len(sys.argv) < 2:
        return

    index = 1
    # Go while there are two values left
    while index < len(sys.argv):
        flag = sys.argv[index]
        index += 1

        # Check flags that require no arguments
        if flag[0] != "-":
            try:
                run_command("load " + flag)
            except:
                print("Error loading file, exiting.")
                exit_command()
            continue
        if flag == "--unsorted":
            __sort = False
            continue
        if flag == "--debug":
            config.debug = True
            continue
            
        if index == len(sys.argv):
            break

        argument = sys.argv[index]
        index += 1

        if flag == "-p" or flag == "--prompt":
            __prompt = argument
        elif flag == "-c" or flag == "--command":
            run_command(argument)

@command("quit")
@command("exit")
@trace
def exit_command():
    """
  exit
  quit          Exits the program."""
    print("Goodbye")
    quit()

@command("help")
@trace
def help_command(command=None):
    """
  help          Displays help for a command if it is given or for all commands otherwise.
                Usage: help [COMMAND]"""
    if not command:
        for command_doc in sorted_documentation():
            print(command_doc)
        return

    if command in __command_actions:
        print(__command_actions[command].__doc__)
    else:
        print("Unrecognized command. Please type 'help' to see the help for all commands.")

@trace
def sorted_documentation():
    return [sorted_function.__doc__ for sorted_function in sorted({command_function for command_function in __command_actions.values()}, key=lambda f: f.__name__)]

@key_command("print")
@key_command("cat")
@key_command("view")
@trace
def view_command(property_path=None):
    """
  print
  cat
  view          Displays the loaded JSON document, if there is one. Otherwise does 
                nothing. You can give it a property path to view a smaller part of
                the document.
                Usage: print [PROPERTY]"""
    global __last_viewed

    __last_viewed = property_path
    print(config.to_string(property_path))

@file_command("open")
@file_command("load")
@trace
def load_command(file_path):
    """
  open
  load          Opens a new file and loads it's contents into memory, where it can
                be worked with.
                Usage: load FILE"""
    config.load(file_path, __sort)

@command("pwd")
@command("cwd")
@trace
def cwd_command():
    """
  pwd
  cwd           Shows the present working directory. Paths to files are relative
                to this path.
                Usage: pwd"""
    print(os.getcwd())

@file_command("cd")
@trace
def cd_command(path):
    """
  cd            Changes the present working directory.
                Usage: cd PATH"""
    os.chdir(path)

@key_command("keys")
@key_command("ls")
@trace
def keys_command(property_path=None):
    """
  ls
  keys          Displays all the keys at a given path. If no property path is
                given then all the keys at the top level of the document will
                be displayed.
                Usage: keys [PROPERTY]"""
    keys = config.keys_at(property_path)
    for key in sorted(keys):
        print("{0:.<70}{1:.>10}".format(key, keys[key]))

@key_command("edit")
@key_command("set")
@trace
def set_command(property_path, value):
    """
  edit
  set           Requires a key path and a value. Will set the value at the
                key path to the supplied value. This operation will create the
                property path if it doesn't already exist.

                To set a value to be an object, you must surround the keys
                with quotes. Embed quotes in your value with \".
                Usage: set PROPERTY VALUE"""
    config.set_property(property_path, value)

@key_command("del")
@key_command("rm")
@trace
def delete_command(property_path):
    """
  del
  rm            Remove a property from the JSON path. Use "write" to save the
                change.
                Usage: rm PROPERTY"""
    config.remove_property(property_path)

@command("last")
@command("view-last")
@command("print-last")
@trace
def view_last_command():
    """
  last
  view-last 
  print-last    View the last property printed.
                Usage: last"""
    global __last_viewed

    print((__last_viewed + ": " if __last_viewed else "") + config.to_string(__last_viewed))

@command("edit-last")
@command("set-last")
@trace
def set_last_command(property_path, value=None):
    """
  edit-last
  set-last      Set the value at the last property that was printed. If a
                property is given too, it will be added as a property of the
                last printed item.
                Usage: set-last [PROPERTY] VALUE"""

    # For now, if you only send one value, it is the value.
    # I can't keyword call this since I'm calling it dynamically.
    if not value:
        value = property_path
        property_path = ""
    else:
        property_path = "." + property_path

    config.set_property(__last_viewed + property_path, value)

@command("del-last")
@command("rm-last")
@trace
def delete_last_command():
    """
  del-last
  rm-last       Delete the last property that was printed.
                Usage: rm-last"""
    global __last_viewed

    if not __last_viewed:
        print("Last viewed is the top level, cannot delete.")
        return

    config.remove_property(__last_viewed)
    __last_viewed = None

@file_command("write")
@file_command("save")
@trace
def save_command(file_path):
    """
  write
  save          Writes the changes to the document back to disk.
                Usage: save"""
    config.save(file_path)

if __name__ == "__main__":
    main()
