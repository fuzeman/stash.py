from stash.core.modules.base import MappingModule


class Archive(MappingModule):
    __group__ = 'archive'

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
