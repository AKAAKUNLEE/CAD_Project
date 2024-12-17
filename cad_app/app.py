import tkinter as tk
from tkinter import simpledialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from .command_manager import CommandManager
from .file_manager import FileManager
from .plugin_system import PluginManager
from .version_control import VersionControl

class CADApp:
    def __init__(self, root):
        self.root = root
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.command_entry = tk.Entry(root)
        self.command_entry.pack(side=tk.BOTTOM, fill=tk.X)
        self.command_entry.bind("<Return>", self.on_command_entered)

        self.command_manager = CommandManager(self)
        self.file_manager = FileManager("project.json")
        self.plugin_manager = PluginManager()
        self.version_control = VersionControl()

        self.load_initial_state()

    def load_initial_state(self):
        initial_state = self.file_manager.load()
        if initial_state:
            self.version_control.take_snapshot(initial_state)

    def on_command_entered(self, event=None):
        command = self.command_entry.get()
        self.command_entry.delete(0, tk.END)
        try:
            result = self.command_manager.execute(command)
            if result:
                print(result)
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = CADApp(root)
    root.mainloop()