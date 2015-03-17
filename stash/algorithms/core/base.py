class Algorithm(object):
    def __init__(self):
        self._stash = None

    @property
    def stash(self):
        return self._stash

    @stash.setter
    def stash(self, value):
        self._stash = value

    @property
    def archive(self):
        return self.stash.archive

    @property
    def cache(self):
        return self.stash.cache

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

    def __setitem__(self, key, value):
        self.cache[key] = value
