from stash import Stash, SqliteArchive
from stash.lib.six.moves import xrange

import pytest


def fetch(cursor, query):
    result = cursor.execute(query)

    return dict(list(result))


def test_construct():
    st = Stash(SqliteArchive(':memory:', 'one'))
    assert type(st.archive) is SqliteArchive
    assert st.archive.table == 'one'

    with pytest.raises(TypeError):
        # Missing 'table' parameter
        st = Stash('sqlite:///')

    st = Stash('sqlite:///:memory:?table=one')
    assert type(st.archive) is SqliteArchive
    assert st.archive.table == 'one'


def test_set():
    st = Stash('sqlite:///:memory:?table=stash', 'lru:///?capacity=10')

    for x in xrange(5):
        st[x] = str(x)

    st.save()

    # Ensure DB contains correct data
    cursor = st.archive.db.cursor()
    data = fetch(cursor, 'select key, value from "%s"' % st.archive.table)

    for x in xrange(5):
        assert data[x] == str(x)


def test_get():
    st = Stash('sqlite:///:memory:?table=stash', 'lru:///?capacity=10')

    # Fill database with test data
    cursor = st.archive.db.cursor()

    for x in xrange(5):
        cursor.execute('insert into "%s" (key, value) values (?, ?)' % st.archive.table, (x, str(x)))

    # Ensure DB contains correct data
    for x in xrange(5):
        assert st[x] == str(x)

    # Ensure `KeyError` is raised on missing items
    with pytest.raises(KeyError):
        assert st[10]


def test_delete():
    st = Stash('sqlite:///:memory:?table=stash', 'lru:///?capacity=10')

    # Fill database with test data
    cursor = st.archive.db.cursor()

    for x in xrange(5):
        cursor.execute('insert into "%s" (key, value) values (?, ?)' % st.archive.table, (x, str(x)))

    # Ensure DB contains correct data
    for x in xrange(5):
        assert st[x] == str(x)

    # Delete items
    del st[2]
    assert st.get(2) is None

    del st[4]
    assert st.get(4) is None

    # Ensure `KeyError` is raised on missing items
    with pytest.raises(KeyError):
        assert st[10]

    # Ensure DB contains correct data
    data = fetch(cursor, 'select key, value from "%s"' % st.archive.table)

    assert data == {
        0: '0',
        1: '1',
        3: '3'
    }


def test_len():
    st = Stash('sqlite:///:memory:?table=stash', 'lru:///?capacity=10')

    # Fill database with test data
    cursor = st.archive.db.cursor()

    for x in xrange(7):
        cursor.execute('insert into "%s" (key, value) values (?, ?)' % st.archive.table, (x, str(x)))

    # Ensure length matches
    assert len(st.archive) == 7
