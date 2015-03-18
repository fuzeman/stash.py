from stash import JsonPickleSerializer


def test_dumps():
    serializer = JsonPickleSerializer()

    assert serializer.dumps(1234) == '1234'
    assert serializer.dumps('1234') == '"1234"'


def test_loads():
    serializer = JsonPickleSerializer()

    assert serializer.loads('1234') == 1234
    assert serializer.loads('"1234"') == '1234'
