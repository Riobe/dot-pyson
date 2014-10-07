#!/usr/bin/python3

import sys
import os
import readline

import config

__command_actions = {}
__prompt = ">>>"
__sort = True

def command(name):
    def command_decorator(function):
        __command_actions[name] = function
        return function
    return command_decorator

def main():
    global __prompt

    print("JSON configuration utility version (1.0.0)")
    handle_arguments()

    command = ""
    while True:
        user_input = input(__prompt + " ").strip()

        if not user_input:
            continue

        run_command(user_input)


def run_command(command_line):
        command_line = command_line.split(" ")
        command = command_line[0]
        argument = command_line[1:]

        if command in __command_actions:
            try:
                __command_actions[command](*argument)
            except TypeError as error:
                message = error.args[0]
                print(message)
                print("Insufficient arguments supplied.")
                help_command(command)
        else:
            print("Unrecognized command")

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
        if flag == "--unsorted":
            __sort = False
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
def exit_command():
    """
  exit
  quit          Exits the program."""
    print("Goodbye")
    quit()

@command("help")
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

def sorted_documentation():
    return [sorted_function.__doc__ for sorted_function in sorted({command_function for command_function in __command_actions.values()}, key=lambda f: f.__name__)]

@command("print")
@command("cat")
@command("view")
def view_command(property_path=None):
    """
  print
  cat
  view          Displays the loaded JSON document, if there is one. Otherwise does 
                nothing. You can give it a property path to view a smaller part of
                the document.
                Usage: print [PROPERTY]"""
    global __sort

    print(config.to_string(property_path))

@command("open")
@command("load")
def load_command(file_path):
    """
  open
  load          Opens a new file and loads it's contents into memory, where it can
                be worked with.
                Usage: load FILE"""
    config.load(file_path, __sort)

@command("pwd")
@command("cwd")
def cwd_command():
    """
  pwd
  cwd           Shows the present working directory. Paths to files are relative
                to this path.
                Usage: pwd"""
    print(os.getcwd())

@command("cd")
def cd_command(path):
    """
  cd            Changes the present working directory.
                Usage: cd PATH"""
    os.chdir(path)

@command("keys")
def keys_command(property_path):
    """
  keys          Displays all the keys at a given path. If no property path is
                given then all the keys at the top level of the document will
                be displayed.
                Usage: keys [PROPERTY]"""
    for key in sorted(config.keys_at(property_path)):
        print(key)

@command("edit")
@command("set")
def edit_command(property_path, value):
    """
  set
  edit          Requires a key path and a value. Will set the value at the
                key path to the supplied value. This operation will create the
                property path if it doesn't already exist.
                Usage: set PROPERTY VALUE"""
    print("Not implemented")

@command("del")
@command("rm")
def delete_command(property_path):
    """
  del
  rm            Remove a property from the JSON path. Use "write" to save the
                change.
                Usage: rm PROPERTY"""
    print("Not implemented")

@command("last")
@command("view-last")
@command("print-last")
def view_last_command():
    """
  last
  view-last 
  print-last    View the last property printed.
                Usage: last"""
    print("Not implemented")

@command("edit-last")
@command("set-last")
def edit_last_command(value):
    """
  edit-last
  set-last      Set the value at the last property that was printed. If a
                property is given too, it will be added as a property of the
                last printed item.
                Usage: set-last [PROPERTY] VALUE"""
    print("Not implemented")

@command("del-last")
@command("rm-last")
def delete_last_command():
    """
  del-last
  rm-last       Delete the last property that was printed.
                Usage: rm-last"""
    print("Not implemented")

@command("write")
@command("save")
def save_command(file_path):
    """
  write
  save          Writes the changes to the document back to disk.
                Usage: save"""
    config.save(file_path)

if __name__ == "__main__":
    main()
