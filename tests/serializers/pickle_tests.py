from stash import PickleSerializer
from stash.lib import six

#
# Pickle v0
#

def test_0_basic():
    serializer = PickleSerializer(protocol=0)

    assert serializer.loads(serializer.dumps(1234)) == 1234
    assert serializer.loads(serializer.dumps('1234')) == '1234'


def test_0_unicode():
    serializer = PickleSerializer(protocol=0)

    assert serializer.loads(serializer.dumps(six.u('\xee'))) == six.u('\xee')
    assert serializer.loads(serializer.dumps(six.u('\xae'))) == six.u('\xae')


def test_0_utf8():
    serializer = PickleSerializer(protocol=0)

    assert serializer.loads(serializer.dumps('\xc3\xae')) == '\xc3\xae'
    assert serializer.loads(serializer.dumps('\xc2\xae')) == '\xc2\xae'


def test_0_escape():
    serializer = PickleSerializer(protocol=0)

    assert serializer.loads(serializer.dumps('\\use')) == '\\use'

#
# Pickle v1
#

def test_1_basic():
    serializer = PickleSerializer(protocol=1)

    assert serializer.loads(serializer.dumps(1234)) == 1234
    assert serializer.loads(serializer.dumps('1234')) == '1234'


def test_1_unicode():
    serializer = PickleSerializer(protocol=1)

    assert serializer.loads(serializer.dumps(six.u('\xee'))) == six.u('\xee')
    assert serializer.loads(serializer.dumps(six.u('\xae'))) == six.u('\xae')


def test_1_utf8():
    serializer = PickleSerializer(protocol=1)

    assert serializer.loads(serializer.dumps('\xc3\xae')) == '\xc3\xae'
    assert serializer.loads(serializer.dumps('\xc2\xae')) == '\xc2\xae'


def test_1_escape():
    serializer = PickleSerializer(protocol=1)

    assert serializer.loads(serializer.dumps('\\use')) == '\\use'

#
# Pickle v2
#

def test_2_basic():
    serializer = PickleSerializer(protocol=2)

    assert serializer.loads(serializer.dumps(1234)) == 1234
    assert serializer.loads(serializer.dumps('1234')) == '1234'


def test_2_unicode():
    serializer = PickleSerializer(protocol=2)

    assert serializer.loads(serializer.dumps(six.u('\xee'))) == six.u('\xee')
    assert serializer.loads(serializer.dumps(six.u('\xae'))) == six.u('\xae')


def test_2_utf8():
    serializer = PickleSerializer(protocol=2)

    assert serializer.loads(serializer.dumps('\xc3\xae')) == '\xc3\xae'
    assert serializer.loads(serializer.dumps('\xc2\xae')) == '\xc2\xae'


def test_2_escape():
    serializer = PickleSerializer(protocol=2)

    assert serializer.loads(serializer.dumps('\\use')) == '\\use'
