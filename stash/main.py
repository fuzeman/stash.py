from collections import MutableMapping


class Stash(MutableMapping):
    def __init__(self, algorithm, archive, cache):
        self.algorithm = algorithm
        self.algorithm.stash = self

        self.archive = archive
        self.cache = cache

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
