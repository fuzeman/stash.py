from stash import PickleSerializer


def test_basic():
    serializer = PickleSerializer()

    assert serializer.loads(serializer.dumps(1234)) == 1234
    assert serializer.loads(serializer.dumps('1234')) == '1234'
