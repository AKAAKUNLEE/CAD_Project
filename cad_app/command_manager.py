from abc import ABC, abstractmethod

class Command(ABC):
    def __init__(self, name, func, description=""):
        self.name = name
        self.func = func
        self.description = description

class CommandManager:
    def __init__(self, app):
        self.commands = {}
        self.app = app

    def add_command(self, command: Command):
        self.commands[command.name] = command

    def execute(self, cmd_str):
        parts = cmd_str.split()
        if not parts or parts[0] not in self.commands:
            raise ValueError("Unknown command")
        try:
            self.commands[parts[0]].func(parts[1:])
        except Exception as e:
            print(f"Error executing {parts[0]}: {e}")