from stash import Stash, LruAlgorithm, SqliteArchive, MemoryCache

if __name__ == '__main__':
    s = Stash(LruAlgorithm(), SqliteArchive('basic.db', 'stash'), MemoryCache())

    if '1' not in s:
        print "s['1'] = 1"
        s['1'] = 1

    print "s['1'] = %r" % s['1']

    s.flush()

    print 'len(s.cache): %r' % len(s.cache)
    print 'len(s.archive): %r' % len(s.archive)

    print "del s['1']"
    del s['1']

    print 'len(s.cache): %r' % len(s.cache)
    print 'len(s.archive): %r' % len(s.archive)
