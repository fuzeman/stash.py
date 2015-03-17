from stash.core.modules.manager import ModuleManager

from collections import MutableMapping


class Stash(MutableMapping):
    def __init__(self, archive, algorithm='lru:///', serializer='none:///', cache='memory:///', hash_key=None):
        # Construct modules
        self.archive = ModuleManager.construct(self, 'archive', archive)
        self.algorithm = ModuleManager.construct(self, 'algorithm', algorithm)
        self.serializer = ModuleManager.construct(self, 'serializer', serializer)
        self.cache = ModuleManager.construct(self, 'cache', cache)

        self.hash_key = hash_key or (lambda key: key)

    def flush(self):
        # Update `archive` with the items in `cache`
        self.archive.update(self.cache)

    def save(self):
        # Flush items from `cache` to `archive`
        self.flush()

        # Ensure `archive` is completely saved
        self.archive.save()

    def __delitem__(self, key):
        del self.algorithm[key]

    def __getitem__(self, key):
        return self.algorithm[key]

    def __iter__(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __setitem__(self, key, value):
        self.algorithm[key] = value
