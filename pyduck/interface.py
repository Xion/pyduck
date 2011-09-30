'''
Definition of pyduck interfaces' metaclass.

Created on 2011-09-21

@author: xion
'''
from method import Method
import inspect


class InterfaceMeta(type):
    ''' Metaclass for interfaces. '''
    
    def __new__(meta, class_name, bases, class_dict): #@NoSelf
        ''' Creates the new interface. '''
        methods = get_functions(class_dict)
        iface_dict = build_iface_dict(methods)
        
        internals = get_internals(class_dict)
        iface_dict.update(internals)
        
        return type.__new__(meta, class_name, bases, iface_dict)
    
    def __instancecheck__(iface, object_or_class): #@NoSelf
        ''' Custom instance checking. Causes isinstance() to verify interface. '''
        return implements(object_or_class, iface)
    
    def __subclasscheck__(iface, cls): #@NoSelf
        ''' Custom subclass checking. Causes issubclass() to verify interface
        (including verification of "strictness" relation for two interfaces). '''
        meta = getattr(cls, '__metaclass__', None)
        if meta and meta == InterfaceMeta:
            checked_iface = cls
            return contains(checked_iface, iface)
        else:
            return implements(cls, iface)


def implements(object_or_class, interface):
    ''' Verifies whether given object or class implements specified interface. '''
    for name, method in interface.__dict__.iteritems():
        if name.startswith('_'):   continue
        member = getattr(object_or_class, name, None)
        if not (member and inspect.ismethod(member)):
            return False
        if not method.conforms_with(member):
            return False
        
    return True

def contains(checked_interface, template_interface):
    ''' Verifies whether first interface is at least as strict as the second one. '''
    for name, method in template_interface.__dict__.iteritems():
        if name.startswith('_'):   continue
        member = getattr(checked_interface, name, None)
        if not member:  return False
        if not method.conforms_with(member):
            return False
        
    return True


###############################################################################
# Helper functions        

def get_functions(class_dict):
    return filter(inspect.isfunction, class_dict.itervalues())

def get_internals(class_dict):
    is_internal = lambda name: name.startswith('__') and name.endswith('__')
    return dict((k, v) for k, v in class_dict.iteritems() if is_internal(k))

def build_iface_dict(methods):
    res = {}
    for method in methods:
        res[method.func_name] = Method(method)
    return res


###############################################################################
# Interface class

class Interface(object):
    ''' Base class for interfaces. It automatically uses the interface metaclass. '''
    __metaclass__ = InterfaceMeta

