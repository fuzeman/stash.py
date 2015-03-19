from stash.algorithms.core.base import Algorithm
from stash.core.helpers import to_integer
from stash.lib.six.moves import xrange

from llist import dllist
import logging

log = logging.getLogger(__name__)


class LruAlgorithm(Algorithm):
    __key__ = 'lru'

    def __init__(self, capacity=100):
        super(LruAlgorithm, self).__init__()

        self.capacity = to_integer(capacity)

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

            # Create node for `key`
            self.create(key)

            return value
        except KeyError:
            # Try load `key` from `archive`
            return self.load(key)

    def __setitem__(self, key, value):
        # Store `value` in cache
        self.cache[key] = value

        # Create node for `key`
        self.create(key)

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

    def create(self, key):
        if key in self.nodes:
            # Move node to the front of `queue`
            self.touch(key)
        else:
            # Store node in `queue`
            self.nodes[key] = self.queue.appendleft(key)

        # Compact `cache`
        self.compact()

    def load(self, key):
        # Load `key` from `archive`
        self[key] = self.archive[key]

        return self.cache[key]

    def touch(self, key):
        node = self.nodes[key]

        # Remove `node` from `queue`
        self.queue.remove(node)

        # Append `node` to the start of `queue`
        self.nodes[key] = self.queue.appendleft(node)
