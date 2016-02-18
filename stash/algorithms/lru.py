from stash.algorithms.core.base import Algorithm
from stash.algorithms.core.prime_context import PrimeContext
from stash.core.helpers import to_integer
from stash.lib.six.moves import xrange, _thread

try:
    from llist import dllist
except ImportError:
    try:
        from pyllist import dllist
    except ImportError:
        dllist = None

from threading import Lock
import collections
import logging

log = logging.getLogger(__name__)


class LruAlgorithm(Algorithm):
    __key__ = 'lru'

    def __init__(self, capacity=100, compact='auto', compact_threshold=200):
        super(LruAlgorithm, self).__init__()

        if dllist is None:
            raise Exception('Unable to construct lru:// - "llist" and "pyllist" modules are not available')

        self.capacity = to_integer(capacity, 100)

        self.compact_mode = compact
        self.compact_threshold = to_integer(compact_threshold, 200)

        self.queue = dllist()
        self.nodes = {}

        self._buffers = {}
        self._release_lock = Lock()

    def __delitem__(self, key):
        try:
            node = self.nodes.pop(key)

            # Remove `node` from `queue`
            self.queue.remove(node)
        except KeyError:
            pass

        # Remove `key` from `cache` and `archive`
        return super(LruAlgorithm, self).__delitem__(key)

    def __getitem__(self, key):
        # Try retrieve value from `prime_buffer`
        try:
            buffer = self._buffers.get(_thread.get_ident())

            if buffer is not None:
                return buffer[key]
        except KeyError:
            pass

        # Try retrieve value from `cache`
        try:
            value = self.cache[key]

            # Ensure node for `key` exists
            self.create(key)

            return value
        except KeyError:
            pass

        # Try load `key` from `archive`
        return self.load(key)

    def __setitem__(self, key, value):
        # Store `value` in cache
        self.cache[key] = value

        # Create node for `key`
        self.create(key)

    def compact(self, force=False):
        count = len(self.nodes)

        if count <= self.capacity:
            return

        if not force and count <= self.compact_threshold:
            return

        self.release_items(count - self.capacity)

    def delete(self, keys):
        if not keys:
            return

        if not isinstance(keys, collections.Iterable):
            keys = [keys]

        for key in keys:
            try:
                node = self.nodes.pop(key)

                # Remove `node` from `queue`
                self.queue.remove(node)
            except KeyError:
                pass

        # Remove keys from `cache` and `archive`
        return super(LruAlgorithm, self).delete(keys)

    def release(self, key=None, force=False):
        if force:
            # Wait until release can be started
            self._release_lock.acquire()
        elif not self._release_lock.acquire(False):
            # Release already running
            return False

        try:
            self._release(key)
        finally:
            self._release_lock.release()

    def _release(self, key=None):
        if key is None:
            key = self.queue.popright()

        # Move item to archive
        self.archive[key] = self.cache.pop(key)

        try:
            # Remove from `nodes`
            del self.nodes[key]
        except KeyError:
            pass

    def release_items(self, count=None, keys=None, force=False):
        if force:
            # Wait until release can be started
            self._release_lock.acquire()
        elif not self._release_lock.acquire(False):
            # Release already running
            return False

        try:
            # Build item iterator
            iterator = self._release_items_iterator(count, keys)

            # Move items to archive
            self.archive.set_items(iterator())
            return True
        finally:
            self._release_lock.release()

    def _release_items_iterator(self, count=None, keys=None):
        if count is not None:
            def iterator():

                for x in xrange(count):
                    # Pop next item from `queue`
                    key = self.queue.popright()

                    try:
                        # Delete from `nodes`
                        del self.nodes[key]

                        # Yield item
                        yield key, self.cache.pop(key)
                    except KeyError:
                        continue

            return iterator

        if keys is not None:
            def iterator():
                for key in keys:
                    # Remove from `queue
                    self.queue.remove(key)

                    try:
                        # Delete from `nodes`
                        del self.nodes[key]

                        # Yield item
                        yield key, self.cache.pop(key)
                    except KeyError:
                        continue

            return iterator

        raise ValueError('Either "count" or "keys" is required')

    def prime(self, keys=None, force=False):
        if keys is not None:
            # Filter keys to ensure we only load ones that don't exist
            keys = [
                key for key in keys
                if key not in self.cache
            ]

        # Iterate over archive items
        items = self.archive.get_items(keys)

        buffer = {}
        context = PrimeContext(self, buffer)

        for key, value in items:
            # Store `value` in cache
            buffer[key] = value

        return context

    def create(self, key, compact=True):
        try:
            # Move node to the front of `queue`
            self.touch(key)
        except KeyError:
            # Store node in `queue`
            self.nodes[key] = self.queue.appendleft(key)

            # Compact `cache` (if enabled)
            if compact and self.compact_mode == 'auto':
                self.compact()

    def load(self, key):
        # Load `key` from `archive`
        self[key] = self.archive[key]

        return self.cache[key]

    def touch(self, key):
        node = self.nodes[key]

        try:
            # Remove `node` from `queue`
            self.queue.remove(node)
        except ValueError:
            # Node doesn't exist in queue
            pass

        # Append `node` to the start of `queue`
        self.nodes[key] = self.queue.appendleft(node)
