#!/usr/bin/python3

import sys
import os

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
            command_actions[command](argument)
        else:
            print("Unrecognized command")


@command("exit")
def exit_command(*args):
    print("Goodbye")
    quit()

@command("happy")
def happy_command(about, *args):
    print("We're happy about: " + about)

@command("view")
def view_command(*args):
#print(config.print())
    config.view()

@command("load")
def load_command(file_path, *args):
    config.load(file_path)

@command("cwd")
def cwd_command(*args):
    print(os.getcwd())

@command("dbg")
def debug_command(*args):
    config.debug()

if __name__ == "__main__":
    main()
