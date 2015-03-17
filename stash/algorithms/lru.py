from stash.algorithms.core.base import Algorithm

from llist import dllist
import logging

log = logging.getLogger(__name__)


class LruAlgorithm(Algorithm):
    def __init__(self, capacity=100):
        super(LruAlgorithm, self).__init__()

        self.capacity = capacity

        self.queue = dllist()
        self.nodes = {}

    def __delitem__(self, key):
        try:
            node = self.nodes.pop(key)

            # Remove `node` from `queue`
            self.queue.remove(node)
        except KeyError:
            pass

        # Remove value from `cache` and `archive`
        return super(LruAlgorithm, self).__delitem__(key)

    def __getitem__(self, key):
        try:
            # Try retrieve value from `cache`
            value = self.cache[key]

            # Move node to the front of `queue`
            self.touch(key)

            return value
        except KeyError:
            # Try load `key` from `archive`
            return self.load(key)

    def __setitem__(self, key, value):
        if key in self.nodes:
            # Move node to the front of `queue`
            self.touch(key)
        else:
            # Store node in `queue`
            self.nodes[key] = self.queue.appendleft(key)

        # Store `value` in cache
        self.cache[key] = value

        # Compact `cache`
        self.compact()

    def compact(self):
        count = len(self.nodes)

        if count <= self.capacity:
            return

        for x in xrange(count - self.capacity):
            self.release()

    def release(self, key=None):
        if key is None:
            key = self.queue.popright()

        # Move item to archive
        self.archive[key] = self.cache.pop(key)

        # Remove from `nodes`
        del self.nodes[key]

        log.debug('release(%r)', key)

    def load(self, key):
        # Try load `key` from `archive`
        self[key] = self.archive[key]

        log.debug('load(%r)', key)

        return self.cache[key]

    def touch(self, key):
        node = self.nodes[key]

        # Remove `node` from `queue`
        self.queue.remove(node)

        # Append `node` to the start of `queue`
        self.nodes[key] = self.queue.appendleft(node)

        log.debug('touch(%r)', key)
