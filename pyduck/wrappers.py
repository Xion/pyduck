'''
Module with wrappers for objects that are known to
implement pyduck interfaces.

Created on 2011-10-05

@author: xion
'''
from pyduck.interface import isinterface
from pyduck.decorators import ExpectedParametersDecorator, ReturnValueDecorator
from pyduck.method import Method


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
        ''' Wraps specified object's methods in @expects/@returns decorators,
        according to those defined on interface's method.
        '''
        for method_name, method in self._interface.__dict__.iteritems():
            if not isinstance(method, Method):  continue
            if not method.is_checked():         continue
            
            obj_method = getattr(obj, method_name, None)
            if not obj_method:
                exc_tuple = (obj, method_name, self._interface.__name__)
                raise TypeError, "Object (%r) does have required method %s of interface %s" % exc_tuple
            
            # decorate with @returns
            if method._returns:
                returns_decorator = ReturnValueDecorator(method._returns)
                obj_method = returns_decorator(obj_method)
            
            # decorate with @expects
            if method._arguments:
                expects_decorator = ExpectedParametersDecorator()
                expects_decorator.arg_spec = method._arguments
                obj_method = expects_decorator(obj_method)
                
            setattr(obj, method_name, obj_method)
            
        return obj


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
