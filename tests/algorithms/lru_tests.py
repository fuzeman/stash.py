from stash import Stash, LruAlgorithm, MemoryArchive, MemoryCache


def test_construct():
    st = Stash(MemoryArchive(), LruAlgorithm)
    assert type(st.algorithm) is LruAlgorithm

    st = Stash(MemoryArchive(), 'lru:///')
    assert type(st.algorithm) is LruAlgorithm

    st = Stash(MemoryArchive(), 'lru:///?capacity=64')
    assert type(st.algorithm) is LruAlgorithm
    assert st.algorithm.capacity == 64


def test_set():
    st = Stash(MemoryArchive(), LruAlgorithm(10))

    # Fill with numbers: 1 - 10
    for x in xrange(1, 11):
        st[x] = str(x)

    assert list(st.cache) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    assert list(st.algorithm.nodes) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert list(st.algorithm.queue) == [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]


def test_get():
    st = Stash(MemoryArchive({3: '3', 4: '4'}), LruAlgorithm(10), cache=MemoryCache({1: '1', 2: '2'}))

    # Ensure numbers 1 - 4 exist
    for x in xrange(1, 5):
        assert st[x] == str(x)


def test_touch():
    st = Stash(MemoryArchive(), LruAlgorithm(10))

    # Fill with numbers: 1 - 10
    for x in xrange(1, 11):
        st[x] = str(x)

    # Bump numbers: 1 - 5
    for x in xrange(1, 6):
        st[x] = str(x)

    assert list(st.cache) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    assert list(st.algorithm.nodes) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert list(st.algorithm.queue) == [5, 4, 3, 2, 1, 10, 9, 8, 7, 6]


def test_archive():
    st = Stash(MemoryArchive(), LruAlgorithm(10))

    # Fill with numbers: 1 - 10
    for x in xrange(1, 11):
        st[x] = str(x)

    # Bump numbers: 1 - 5
    for x in xrange(1, 6):
        st[x] = str(x)

    # Fill with numbers: 21 - 25
    for x in xrange(21, 26):
        st[x] = str(x)

    assert list(st.archive) == [8, 9, 10, 6, 7]
    assert list(st.cache) == [1, 2, 3, 4, 5, 21, 22, 23, 24, 25]

    assert list(st.algorithm.nodes) == [1, 2, 3, 4, 5, 21, 22, 23, 24, 25]
    assert list(st.algorithm.queue) == [25, 24, 23, 22, 21, 5, 4, 3, 2, 1]
