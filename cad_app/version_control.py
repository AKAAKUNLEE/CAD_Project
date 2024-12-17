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