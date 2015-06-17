from stash import PickleSerializer
from stash.lib import six


def test_basic():
    serializer = PickleSerializer()

    assert serializer.loads(serializer.dumps(1234)) == 1234
    assert serializer.loads(serializer.dumps('1234')) == '1234'


def test_unicode():
    serializer = PickleSerializer()

    assert serializer.loads(serializer.dumps(six.u('\xee'))) == six.u('\xee')
    assert serializer.loads(serializer.dumps(six.u('\xae'))) == six.u('\xae')


def test_utf8():
    serializer = PickleSerializer()

    assert serializer.loads(serializer.dumps('\xc3\xae')) == '\xc3\xae'
    assert serializer.loads(serializer.dumps('\xc2\xae')) == '\xc2\xae'
