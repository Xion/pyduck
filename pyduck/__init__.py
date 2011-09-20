

class InterfaceMeta(type):
    ''' Metaclass for interfaces. '''
    pass


class Interface(object):
    ''' Base class for interfaces. It automatically uses the interface metaclass. '''
    __metaclass__ = InterfaceMeta
    
    
def implements(obj, interface):
    pass
