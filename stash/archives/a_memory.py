from stash.archives.core.base import Archive


class MemoryArchive(Archive):
    __key__ = 'memory'

    def __init__(self, initial=None):
        super(MemoryArchive, self).__init__()

        self.data = initial or {}

    def save(self):
        pass

    def __delitem__(self, key):
        key = self.hash_key(key)

        del self.data[key]

    def __getitem__(self, key):
        key = self.hash_key(key)

        return self.data[key]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __setitem__(self, key, value):
        key = self.hash_key(key)

        self.data[key] = value
