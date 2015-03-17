from stash.core.modules.base import MappingModule


class Archive(MappingModule):
    __group__ = 'archive'

    @property
    def serializer(self):
        return self.stash.serializer

    def dumps(self, value):
        return self.serializer.dumps(value)

    def loads(self, value):
        return self.serializer.loads(value)

    def save(self):
        raise NotImplementedError

    def __delitem__(self, key):
        raise NotImplementedError

    def __getitem__(self, key):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __setitem__(self, key, value):
        raise NotImplementedError
