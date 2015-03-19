import logging
logging.basicConfig(level=logging.DEBUG)

from stash import Stash
from stash.lib.six.moves import xrange


if __name__ == '__main__':
    s = Stash('apsw:///apsw_archive.db?table=stash', 'lru:///?capacity=5')

    for x in xrange(5):
        s[str(x)] = x

    for x in xrange(2):
        s[str(x)] = x

    for x in xrange(10, 13):
        s[str(x)] = x

    s.flush()

    print 'len(s.cache): %r' % len(s.cache)
    print 'len(s.archive): %r' % len(s.archive)

    for x in xrange(5):
        assert s[str(x)] == x

    print "del s['1']"
    del s['1']

    print 'len(s.cache): %r' % len(s.cache)
    print 'len(s.archive): %r' % len(s.archive)
