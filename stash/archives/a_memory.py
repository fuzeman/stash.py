from stash.archives.core.base import Archive


class MemoryArchive(Archive):
    def __init__(self, initial=None):
        self.data = initial or {}

    def save(self):
        pass

    def __delitem__(self, key):
        del self.data[key]

    def __getitem__(self, key):
        return self.data[key]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __setitem__(self, key, value):
        self.data[key] = value
