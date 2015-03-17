from stash.serializers.core.base import Serializer

import pickle


class PickleSerializer(Serializer):
    __key__ = 'pickle'

    def dumps(self, value):
        return pickle.dumps(value)

    def loads(self, value):
        return pickle.loads(value)
