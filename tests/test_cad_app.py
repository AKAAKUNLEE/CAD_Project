import unittest
from cad_app.command_manager import CommandManager
from cad_app.file_manager import FileManager
from cad_app.version_control import VersionControl

class TestCADApp(unittest.TestCase):
    def setUp(self):
        self.command_manager = CommandManager(None)
        self.file_manager = FileManager("test_project.json")
        self.version_control = VersionControl()

    def test_command_manager(self):
        self.command_manager.add_command(Command("test", lambda params: "Test command executed"))
        result = self.command_manager.execute("test")
        self.assertEqual(result, "Test command executed")

    def test_file_manager(self):
        data = {"key": "value"}
        self.file_manager.save(data)
        loaded_data = self.file_manager.load()
        self.assertEqual(loaded_data, data)

    def test_version_control(self):
        state = {"state": "initial"}
        self.version_control.take_snapshot(state)
        restored_state = self.version_control.revert_to_snapshot(0)
        self.assertEqual(restored_state, state)

if __name__ == '__main__':
    unittest.main()