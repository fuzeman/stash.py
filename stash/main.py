from collections import MutableMapping


class Stash(MutableMapping):
    def __init__(self, algorithm, archive, cache):
        self.algorithm = algorithm
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
        success = False

        try:
            # Delete `key` from `archive`
            del self.archive[key]
            success = True
        except KeyError:
            pass

        try:
            # Delete `key` from `cache`
            del self.cache[key]
            success = True
        except KeyError:
            pass

        if not success:
            # Couldn't find `key` in `archive` or `cache`
            raise KeyError(key)

    def __getitem__(self, key):
        try:
            return self.cache[key]
        except KeyError:
            # Load item into `cache`
            self.cache[key] = self.archive[key]

            return self.cache[key]

    def __iter__(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __setitem__(self, key, value):
        self.cache[key] = value
