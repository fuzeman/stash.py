from stash import Stash
from stash.lib.six.moves import xrange

from threading import Semaphore, Thread
import pytest
import random
import sys


class TestConcurrency:
    def setup_method(self, *args):
        self.st = Stash('apsw:///:memory:?table=stash', 'lru:///?capacity=10')

    def teardown_method(self, *args):
        self.st = None

    #
    # Tests
    #

    def test_short(self):
        self.run({
            'get':   (10, 500),
            'set':   (10, 500),
            'flush': ( 5, 250)
        })

    @pytest.mark.slow
    def test_long(self):
        self.run({
            'get':   (20, 1000),
            'set':   (20, 1000),
            'flush': (10,  500)
        })

    #
    # Tasks
    #

    def run(self, tasks):
        # Setup test
        self.exc_info = None
        self.running = True

        self.active = Semaphore()

        # Spawn threads
        self.start(tasks)

        # Wait for threads to complete
        self.wait(tasks)

        # Raise any exception captured in threads
        if self.exc_info:
            raise self.exc_info[0], self.exc_info[1], self.exc_info[2]

    def start(self, tasks):
        count = sum([
            threads
            for (threads, _) in tasks.values()
        ])

        self.active._Semaphore__value = count

        # Start threads
        for mode in ['get', 'set', 'flush']:
            self.start_task(mode, *(tasks.get(mode) or (0, 0)))

    def start_task(self, mode, threads, samples):
        for x in xrange(threads):
            self.start_one(mode, x, samples)

    def start_one(self, mode, id, samples):
        self.active.acquire()

        thread = Thread(name='%s:%s' % (mode, id), target=self.child_run, args=(mode, samples))
        thread.start()

    def wait(self, tasks):
        count = sum([
            threads
            for (threads, _) in tasks.values()
        ])
        remaining = count

        for x in xrange(count):
            self.active.acquire()
            remaining -= 1

    def child_run(self, mode, samples):
        try:
            # Run operations
            func = getattr(self, 'child_%s' % mode, None)

            if func is None:
                raise ValueError('Unknown mode: %r' % mode)

            func(samples)
        except Exception:
            self.exc_info = sys.exc_info()
            self.running = False
        finally:
            self.active.release()

    def child_get(self, samples):
        # Build list of random numbers
        nums = list(xrange(samples))
        random.shuffle(nums)

        # Run operations
        for x in nums:
            if not self.running:
                break

            self.st.get(x)

    def child_set(self, samples):
        # Build list of random numbers
        nums = list(xrange(samples))
        random.shuffle(nums)

        # Run operations
        for x in nums:
            if not self.running:
                break

            self.st[x] = str(x)

    def child_flush(self, samples):
        # Run operations
        for x in xrange(samples):
            if not self.running:
                break

            self.st.flush(force=True)
