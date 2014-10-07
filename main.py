#!/usr/bin/python3

import sys
import os
import readline

import config

command_actions = {}

def command(name):
    def command_decorator(function):
        command_actions[name] = function
        return function
    return command_decorator

def main():
    prompt = ">>>"
    if len(sys.argv) == 3 and (sys.argv[1] == "-p" or sys.argv[1] == "--prompt"):
        prompt = sys.argv[2]

    print("JSON configuration utility version (1.0.0)")

    command = ""
    while True:
        user_input = input(prompt + " ").strip().split(" ")

        if not user_input:
            continue

        command = user_input[0]
        argument = " ".join(user_input[1:])

        if command in command_actions:
            try:
                command_actions[command](argument)
            except TypeError:
                print("Insufficient arguments supplied.")
                help_command(command)
        else:
            print("Unrecognized command")


@command("quit")
@command("exit")
def exit_command(*args):
    print("Goodbye")
    quit()

@command("help")
def help_command(command, *args):
    if not command:
        for command_function in {function for function in command_actions.values()}:
            print(command_function.__doc__)
        return

    if command in command_actions:
        print(command_actions[command].__doc__)
    else:
        print("Unrecognized command. Please type 'help' to see the help for all commands.")

@command("print")
@command("view")
def view_command(key_path, *args):
    config.view()

@command("open")
@command("load")
def load_command(file_path, *args):
    config.load(file_path)

@command("pwd")
@command("cwd")
def cwd_command(*args):
    print(os.getcwd())

@command("keys")
def keys_command(key_path, *args):
    print("Not implemented")

@command("edit")
@command("set")
def edit_command(key_path, value, *args):
    """
  set
  edit       Requires a key path and a value. Will set the value at the
                    key path to the supplied value."""
    print("Not implemented")

@command("del")
@command("rm")
def delete_command(key_path, *args):
    print("Not implemented")

@command("last")
@command("view-last")
def view_last_command(*args):
    print("Not implemented")

@command("edit-last")
@command("set-last")
def edit_last_command(value, *args):
    print("Not implemented")

@command("del-last")
@command("rm-last")
def delete_last_command(*args):
    print("Not implemented")

@command("write")
@command("save")
def save_command(*args):
    print("Not implemented")

if __name__ == "__main__":
    main()
