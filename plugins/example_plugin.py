from cad_app.command_manager import Command

class CustomToolPlugin:
    def __init__(self, manager):
        self.manager = manager

    def activate(self):
        print("Custom tool plugin activated.")
        self.manager.command_manager.add_command(
            Command("custom_tool", lambda params: print("Using custom tool"), "A custom drawing tool"))

    def deactivate(self):
        print("Custom tool plugin deactivated.")