import logging
logging.basicConfig(level=logging.DEBUG)

from stash import Stash, LruAlgorithm, SqliteArchive, MemoryCache


if __name__ == '__main__':
    s = Stash(LruAlgorithm(5), SqliteArchive('basic.db', 'stash'), MemoryCache())

    for x in xrange(5):
        s[str(x)] = x

    for x in xrange(2):
        s[str(x)] = x

    for x in xrange(10, 13):
        s[str(x)] = x

    s.flush()

    print 'len(s.cache): %r' % len(s.cache)
    print 'len(s.archive): %r' % len(s.archive)

    print "del s['1']"
    del s['1']

    print 'len(s.cache): %r' % len(s.cache)
    print 'len(s.archive): %r' % len(s.archive)
