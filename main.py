#!/usr/bin/python3

import sys
import inspect

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
            command_function = command_actions[command]

            if (argument_count(command_function)):
                command_function(argument)
            else:
                command_function()
        else:
            print("Unrecognized command")


@command("exit")
def exit_command():
    print("Goodbye")
    quit()

@command("happy")
def happy_command(about):
    print("We're happy about: " + about)

def argument_count(function):
    return len(inspect.getargspec(command_function)[0])

if __name__ == "__main__":
    main()
