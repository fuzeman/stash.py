from stash.serializers.core.base import Serializer

import jsonpickle


class JsonPickleSerializer(Serializer):
    __key__ = 'jsonpickle'

    def dumps(self, value):
        return jsonpickle.encode(value)

    def loads(self, value):
        return jsonpickle.decode(value)
