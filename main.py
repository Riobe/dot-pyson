#!/usr/bin/python3

import sys
import os
import readline

import config

command_actions = {}
__prompt = ">>>"

def command(name):
    def command_decorator(function):
        command_actions[name] = function
        return function
    return command_decorator

def main():
    global __prompt

    handle_arguments()

    print("JSON configuration utility version (1.0.0)")

    command = ""
    while True:
        user_input = input(__prompt + " ").strip()

        if not user_input:
            continue

        run_command(user_input)


def run_command(command_line):
        command_line = command_line.split(" ")
        command = command_line[0]
        argument = " ".join(command_line[1:])

        if command in command_actions:
            try:
                command_actions[command](argument)
            except TypeError:
                print("Insufficient arguments supplied.")
                help_command(command)
        else:
            print("Unrecognized command")

def handle_arguments():
    global __prompt

    # No arguments.
    if len(sys.argv) < 2:
        return

    index = 1
    # Go while there are two values left
    while index < len(sys.argv)-1:
        flag = sys.argv[index]
        argument = sys.argv[index+1]
        index += 2

        if flag == "-p" or flag == "--prompt":
            __prompt = argument
        if flag == "-c" or flag == "--command":
            run_command(argument)

@command("quit")
@command("exit")
def exit_command(*args):
    """
  exit
  quit          Exits the program."""
    print("Goodbye")
    quit()

@command("help")
def help_command(command, *args):
    """
  help          Displays help for a command if it is given or for all commands otherwise.
                Usage: help [COMMAND]"""
    if not command:
        for command_doc in sorted_documentation():
            print(command_doc)
        return

    if command in command_actions:
        print(command_actions[command].__doc__)
    else:
        print("Unrecognized command. Please type 'help' to see the help for all commands.")

def sorted_documentation():
    return [sorted_function.__doc__ for sorted_function in sorted({command_function for command_function in command_actions.values()}, key=lambda f: f.__name__)]

@command("print")
@command("view")
def view_command(property_path, *args):
    """
  print
  view          Displays the loaded JSON document, if there is one. Otherwise does 
                nothing. You can give it a property path to view a smaller part of
                the document.
                Usage: print [PROPERTY]"""
    print(config.to_string())

@command("open")
@command("load")
def load_command(file_path, *args):
    """
  open
  load          Opens a new file and loads it's contents into memory, where it can
                be worked with.
                Usage: load FILE"""
    config.load(file_path)

@command("pwd")
@command("cwd")
def cwd_command(*args):
    """
  pwd
  cwd           Shows the present working directory. Paths to files are relative
                to this path.
                Usage: pwd"""
    print(os.getcwd())

@command("cd")
def cd_command(path, *args):
    """
  cd            Changes the present working directory.
                Usage: cd PATH"""
    os.chdir(path)

@command("keys")
def keys_command(property_path, *args):
    """
  keys          Displays all the keys at a given path. If no property path is
                given then all the keys at the top level of the document will
                be displayed.
                Usage: keys [PROPERTY]"""
    for key in sorted(config.keys_at(property_path)):
        print(key)

@command("edit")
@command("set")
def edit_command(property_path, value, *args):
    """
  set
  edit          Requires a key path and a value. Will set the value at the
                key path to the supplied value. This operation will create the
                property path if it doesn't already exist.
                Usage: set PROPERTY VALUE"""
    print("Not implemented")

@command("del")
@command("rm")
def delete_command(property_path, *args):
    """
  del
  rm            Remove a property from the JSON path. Use "write" to save the
                change.
                Usage: rm PROPERTY"""
    print("Not implemented")

@command("last")
@command("view-last")
@command("print-last")
def view_last_command(*args):
    """
  last
  view-last 
  print-last    View the last property printed.
                Usage: last"""
    print("Not implemented")

@command("edit-last")
@command("set-last")
def edit_last_command(value, *args):
    """
  edit-last
  set-last      Set the value at the last property that was printed. If a
                property is given too, it will be added as a property of the
                last printed item.
                Usage: set-last [PROPERTY] VALUE"""
    print("Not implemented")

@command("del-last")
@command("rm-last")
def delete_last_command(*args):
    """
  del-last
  rm-last       Delete the last property that was printed.
                Usage: rm-last"""
    print("Not implemented")

@command("write")
@command("save")
def save_command(*args):
    """
  write
  save          Writes the changes to the document back to disk.
                Usage: save"""
    print("Not implemented")

if __name__ == "__main__":
    main()
