'''
Contains the Method class, which represents a method of an interface
whose existence and signature is being checked against.

Created on 2011-09-21

@author: xion
'''
import inspect


class Method(object):
    ''' Represents the method of an interface. '''

    def __init__(self, actual_method):
        ''' Initializes the object from an actual method. '''
        if not inspect.ismethod(actual_method):
            raise ValueError, "Expected a method, got %r" % actual_method
        
        arg_spec = inspect.getargspec(actual_method)
        arg_names, varargs_name, kwargs_name, _default_values = arg_spec
        
        self.arg_count = len(arg_names)
        self.has_varargs = varargs_name is not None
        self.has_kwargs = kwargs_name is not None
        
    def conforms_with(self, method):
        ''' Checks whether given method is compatible with method signature
        described by this very object. '''
        if isinstance(method, Method):
            method_obj = method
        elif inspect.ismethod(method):
            method_obj = Method(method)
        else:
            raise ValueError, "Expected a method, got %r" % method

        # very simple check for now
        for criteria in ['arg_count', 'has_varargs', 'has_kwargs']:
            if getattr(self, criteria, None) != getattr(method_obj, criteria, None):
                return False
        return True
