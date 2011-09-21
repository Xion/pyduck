from metaclass import InterfaceMeta
import inspect


class Interface(object):
    ''' Base class for interfaces. It automatically uses the interface metaclass. '''
    __metaclass__ = InterfaceMeta
    

def implements(object_or_class, interface):
    ''' Verifies whether given object or class implements specified interface. '''
    return isinstance(object_or_class, interface)
