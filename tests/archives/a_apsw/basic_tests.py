from stash import Stash, ApswArchive
from stash.lib.six.moves import xrange
from stash.lib import six

import pytest


def fetch(cursor, query):
    result = cursor.execute(query)

    return dict(list(result))


def test_construct():
    st = Stash(ApswArchive(':memory:', 'one'))
    assert type(st.archive) is ApswArchive
    assert st.archive.table == 'one'

    with pytest.raises(TypeError):
        # Missing 'table' parameter
        st = Stash('apsw:///')

    st = Stash('apsw:///:memory:?table=one')
    assert type(st.archive) is ApswArchive
    assert st.archive.table == 'one'


def test_set():
    st = Stash('apsw:///:memory:?table=stash', 'lru:///?capacity=10')

    for x in xrange(5):
        st[x] = str(x)

    st.save()

    # Ensure DB contains correct data
    cursor = st.archive.db.cursor()
    data = fetch(cursor, 'select key, value from "%s"' % st.archive.table)

    for x in xrange(5):
        assert str(data[x]) == str(x)


def test_set_unicode():
    st = Stash('apsw:///:memory:?table=stash', 'lru:///?capacity=10')
    values = [six.u('\xae'), six.u('\xaf'), six.u('\xb0')]

    for x in xrange(len(values)):
        st[x] = values[x]

    st.save()

    # Ensure DB contains correct data
    cursor = st.archive.db.cursor()
    data = fetch(cursor, 'select key, value from "%s"' % st.archive.table)

    for x in xrange(len(values)):
        if six.PY3:
            assert ord(six.text_type(data[x])) == ord(values[x])
        else:
            assert ord(str(data[x]).decode('unicode_internal')) == ord(values[x])


def test_set_utf8():
    st = Stash('apsw:///:memory:?table=stash', 'lru:///?capacity=10')
    values = ['\xc2\xae', '\xc2\xaf', '\xc2\xb0']

    for x in xrange(len(values)):
        st[x] = values[x]

    st.save()

    # Ensure DB contains correct data
    cursor = st.archive.db.cursor()
    data = fetch(cursor, 'select key, value from "%s"' % st.archive.table)

    for x in xrange(len(values)):
        assert str(data[x]) == values[x]


def test_get():
    st = Stash('apsw:///:memory:?table=stash', 'lru:///?capacity=10')

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
    st = Stash('apsw:///:memory:?table=stash', 'lru:///?capacity=10')

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
    st = Stash('apsw:///:memory:?table=stash', 'lru:///?capacity=10')

    # Fill database with test data
    cursor = st.archive.db.cursor()

    for x in xrange(7):
        cursor.execute('insert into "%s" (key, value) values (?, ?)' % st.archive.table, (x, str(x)))

    # Ensure length matches
    assert len(st.archive) == 7
