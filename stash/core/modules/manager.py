from urlparse import urlparse, parse_qsl
import inspect
import logging

log = logging.getLogger(__name__)


class ModuleManager(object):
    modules = {}

    @classmethod
    def construct(cls, group, value):
        if isinstance(value, (str, unicode)):
            return cls.from_uri(group, value)

        if inspect.isclass(value):
            return value()

        return value

    @classmethod
    def from_uri(cls, group, uri):
        if group not in cls.modules:
            return None

        result = urlparse(uri)
        key = result.scheme

        if key not in cls.modules[group]:
            return None

        module = cls.modules[group][key]

        # Parse `path`
        args = []

        path = result.path.lstrip('/')

        if path:
            args.append(result.path.lstrip('/'))

        # Parse `query`
        kwargs = dict(parse_qsl(result.query))

        # Construct module
        return module(*args, **kwargs)

    @classmethod
    def register(cls, module):
        group = module.__group__
        key = module.__key__

        if not group or not key:
            log.warn('Unable to register: %r - missing a "__group__" or "__key__" attribute', module)
            return

        if group not in cls.modules:
            cls.modules[group] = {}

        if key in cls.modules[group]:
            log.warn('Unable to register: %r - already registered', module)
            return

        cls.modules[group][key] = module
