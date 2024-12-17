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