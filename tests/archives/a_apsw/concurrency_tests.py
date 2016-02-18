from stash import Stash
from stash.lib.six.moves import xrange

from threading import Semaphore, Thread
import random
import sys


class TestConcurrency:
    def setup_method(self, *args):
        self.st = Stash('apsw:///:memory:?table=stash', 'lru:///?capacity=10')

    def teardown_method(self, *args):
        # TODO self.st.close()
        self.st = None

    def test_threading(self):
        # Setup test
        self.exc_info = None
        self.running = True

        self.active = Semaphore()

        tasks = {
            'get': 10,
            'set': 10,
            'flush': 5
        }

        # Spawn threads
        self.start(tasks)

        # Wait for threads to complete
        self.wait(tasks)

        # Raise any exception captured in threads
        if self.exc_info:
            raise self.exc_info[0], self.exc_info[1], self.exc_info[2]

    def run(self, mode, id):
        try:
            # Run operations
            if mode == 'get':
                self.run_get(mode, id)

            if mode == 'set':
                self.run_set(mode, id)

            if mode == 'flush':
                self.run_flush(mode, id)
        except Exception:
            self.exc_info = sys.exc_info()
            self.running = False
        finally:
            self.active.release()

    def run_get(self, mode, id):
        # Build list of random numbers
        nums = list(xrange(1000))
        random.shuffle(nums)

        # Run operations
        for x in nums:
            if not self.running:
                break

            self.st.get(x)

    def run_set(self, mode, id):
        # Build list of random numbers
        nums = list(xrange(1000))
        random.shuffle(nums)

        # Run operations
        for x in nums:
            if not self.running:
                break

            self.st[x] = str(x)

    def run_flush(self, mode, id):
        # Run operations
        for x in xrange(500):
            if not self.running:
                break

            self.st.flush()

    def start_one(self, mode, id):
        self.active.acquire()

        thread = Thread(name='%s:%s' % (mode, id), target=self.run, args=(mode, id))
        thread.start()

    def start(self, tasks):
        count = sum(tasks.values())

        self.active._Semaphore__value = count

        # Start threads
        for x in xrange(tasks.get('get', 0)):
            self.start_one('get', x)

        for x in xrange(tasks.get('set', 0)):
            self.start_one('set', x)

        for x in xrange(tasks.get('flush', 0)):
            self.start_one('flush', x)

    def wait(self, tasks):
        count = sum(tasks.values())
        remaining = count

        for x in xrange(count):
            self.active.acquire()
            remaining -= 1

if __name__ == '__main__':
    cls = TestConcurrency()

    cls.setup_method()
    cls.test_threading()
