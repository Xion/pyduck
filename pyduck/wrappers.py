'''
Module with wrappers for objects that are known to
implement pyduck interfaces.

Created on 2011-10-05

@author: xion
'''
from pyduck.interface import isinterface


class EnforceWrapper(object):
    ''' The enforce() wrapper. It ensures that given
    object implements particular pyduck interface. Additionally,
    it also allows to  take advantage  of automatic verification
    of @expects declarations on that interface's methods - as if
    they were directly applied to object's methods instead.
    '''
    def __init__(self, iface):
        if not isinterface(iface):
            raise TypeError, "enforce() requires an Interface"
        self._interface = iface

    def __call__(self, obj):
        return self.on(obj)

    def on(self, obj):
        pass


def enforce(iface, obj = None):
    ''' Enforces particular interface on given object.
    It can be used in one of following ways:
    >>> enforce(Interface).on(obj)
    >>> enforce(Interface)(obj)
    >>> enforce(Interface, obj)
    In either case, it returns a proxy object which
    has its methods wrapped in arguments' checks,
    as defined by @expects declarations applied to corresponding
    interface methods.
    '''
    wrapper = EnforceWrapper(iface)
    if obj is None:
        return wrapper
    return wrapper.on(obj)
