from stash import PickleSerializer


def test_dumps():
    serializer = PickleSerializer()

    assert serializer.dumps(1234) == "I1234\n."
    assert serializer.dumps('1234') == "S'1234'\np0\n."


def test_loads():
    serializer = PickleSerializer()

    assert serializer.loads("I1234\n.") == 1234
    assert serializer.loads("S'1234'\np0\n.") == '1234'
