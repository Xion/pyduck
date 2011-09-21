'''
Metaclass for pyduck interfaces.

Created on 2011-09-21

@author: xion
'''
import inspect
from method import Method


class InterfaceMeta(type):
    ''' Metaclass for interfaces. '''
    
    def __new__(meta, class_name, bases, class_dict): #@NoSelf
        ''' Creates the new interface. '''
        methods = get_methods(class_dict)
        iface_dict = build_iface_dict(methods)
        
        internals = get_internals(class_dict)
        iface_dict.update(internals)
        
        return type.__new__(meta, class_name, bases, iface_dict)
    
    def __instancecheck__(iface, object_or_class): #@NoSelf
        ''' Custom instance checking. Causes isinstance() to verify interface. '''
        for name, method_obj in iface.__dict__.iteritems():
            if name.startswith('_'):   continue
            member = getattr(object_or_class, name, None)
            if not (member and inspect.ismethod(member)):
                return False
            if not method_obj.conforms_with(member):
                return False
            
        return True
        

def get_methods(class_dict):
    return filter(inspect.isfunction, class_dict.itervalues())

def build_iface_dict(methods):
    res = {}
    for method in methods:
        res[method.func_name] = Method(method)
    return res

def get_internals(class_dict):
    is_internal = lambda name: name.startswith('__') and name.endswith('__')
    return dict((k, v) for k, v in class_dict.iteritems() if is_internal(k))
