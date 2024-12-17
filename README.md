创建一个Python项目来实现上述需求，可以按照以下步骤进行。我们将使用`tkinter`作为GUI库，并结合`matplotlib`和`pythreejs`来处理二维绘图和三维建模。此外，我们将构建一个简单的插件系统，并实现基本的文件管理和版本控制功能。

### 项目结构

首先，我们定义项目的目录结构：

```
cad_project/
├── cad_app/
│   ├── __init__.py
│   ├── app.py
│   ├── command_manager.py
│   ├── file_manager.py
│   ├── plugin_system.py
│   ├── three_d_modeler.py
│   └── version_control.py
├── plugins/
│   ├── __init__.py
│   └── example_plugin.py
├── tests/
│   ├── __init__.py
│   └── test_cad_app.py
├── README.md
└── setup.py
```

### 创建虚拟环境并安装依赖

在项目根目录下创建并激活虚拟环境，然后安装所需的依赖包：

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install matplotlib pythreejs numpy pytest
```

### 编写核心模块

#### `cad_app/app.py`

这是主应用程序文件，负责初始化和运行CAD应用。

```python
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
```

#### `cad_app/command_manager.py`

命令管理器负责解析和执行用户输入的命令。

```python
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
```

#### `cad_app/file_manager.py`

文件管理器用于保存和加载项目文件。

```python
import json
from pathlib import Path

class FileManager:
    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def save(self, data):
        with open(self.file_path, 'w') as f:
            json.dump(data, f)

    def load(self):
        if not self.file_path.exists():
            return {}
        with open(self.file_path, 'r') as f:
            return json.load(f)
```

#### `cad_app/plugin_system.py`

插件系统允许动态加载和管理插件。

```python
import importlib.util
from abc import ABC, abstractmethod

class PluginBase(ABC):
    def __init__(self, manager):
        self.manager = manager

    @abstractmethod
    def activate(self):
        pass

    @abstractmethod
    def deactivate(self):
        pass

class PluginManager:
    def __init__(self):
        self.plugins = []

    def load_plugin(self, plugin_path):
        spec = importlib.util.spec_from_file_location("plugin", plugin_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        plugin_class = getattr(module, 'PluginClass', None)
        if plugin_class and issubclass(plugin_class, PluginBase):
            plugin = plugin_class(self)
            self.plugins.append(plugin)
            return plugin
        else:
            raise ValueError(f"Invalid plugin at {plugin_path}")

    def activate_plugins(self):
        for plugin in self.plugins:
            plugin.activate()

    def deactivate_plugins(self):
        for plugin in self.plugins:
            plugin.deactivate()
```

#### `cad_app/three_d_modeler.py`

三维建模模块负责处理三维图形的创建和渲染。

```python
from pythreejs import *
import numpy as np

class ThreeDModeler:
    def __init__(self, root):
        self.scene = Scene(children=[AmbientLight(color='#777777')])
        self.camera = PerspectiveCamera(position=[5, 5, 5], up=[0, 0, 1], children=[DirectionalLight(color='white', position=[3, 5, 1], intensity=0.5)])
        self.renderer = Renderer(camera=self.camera, scene=self.scene, background='black', background_opacity=1,
                                 controls=[OrbitControls(controlling=self.camera)])
        self.root = root
        self.embed_3d_view()

    def embed_3d_view(self):
        from IPython.display import display
        widget = self.renderer
        widget.width = 800
        widget.height = 600
        display(widget)

    def add_cube(self, size=1):
        geometry = BoxGeometry(size, size, size)
        material = MeshLambertMaterial(color='red')
        cube = Mesh(geometry, material)
        self.scene.add(cube)
```

#### `cad_app/version_control.py`

版本控制系统帮助用户管理不同版本的工作状态。

```python
class VersionControl:
    def __init__(self):
        self.snapshots = []
        self.current_snapshot_index = -1

    def take_snapshot(self, state):
        if self.current_snapshot_index < len(self.snapshots) - 1:
            self.snapshots = self.snapshots[:self.current_snapshot_index + 1]
        self.snapshots.append(state.copy())
        self.current_snapshot_index += 1

    def revert_to_snapshot(self, index=None):
        if index is None:
            index = self.current_snapshot_index
        if 0 <= index < len(self.snapshots):
            self.current_snapshot_index = index
            return self.snapshots[index].copy()
        else:
            raise IndexError("Snapshot index out of range")
```

### 插件示例

#### `plugins/example_plugin.py`

这是一个简单的插件示例，添加了一个新的绘图命令。

```python
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
```

### 测试用例

#### `tests/test_cad_app.py`

编写单元测试确保各个模块按预期工作。

```python
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
```

### 运行项目

确保所有文件都已正确放置在各自的目录中后，可以通过以下命令启动项目：

```bash
python -m cad_app.app
```

这将启动CAD应用程序的图形界面，你可以开始测试和开发更多功能了。

如果你有特定的需求或者需要进一步的帮助，请随时告诉我！