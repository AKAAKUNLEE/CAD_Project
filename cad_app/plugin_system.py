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
            