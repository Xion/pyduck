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
        if not is_function(actual_method):
            raise ValueError, "Expected method/function, got %r" % actual_method
        
        arg_spec = inspect.getargspec(actual_method)
        arg_names, varargs_name, kwargs_name, default_values = arg_spec
        default_values = default_values or []
        
        self.name = actual_method.func_name
        self.max_args = len(arg_names)
        self.min_args = self.max_args - len(default_values)
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

        # check number of arguments
        self_arg_range = (self.min_args, self.max_args)
        other_arg_range = (method_obj.min_args, method_obj.max_args)
        if not intervals_overlap(self_arg_range, other_arg_range):
            return False
        
        if self.has_varargs != method_obj.has_varargs:  return False
        if self.has_kwargs != method_obj.has_kwargs:    return False
        
        return True


def is_function(func):
    ''' Generalized check for methods and normal functions. '''
    return inspect.ismethod(func) or inspect.isfunction(func)

def intervals_overlap(interval1, interval2):
    ''' Checks whether two intervals overlap.
    Used for comparing number of mandatory and optional arguments. '''
    a1, b1 = interval1
    a2, b2 = interval2
    
    first_before_second = b1 < a2
    second_before_first = b2 < a1
    return not (first_before_second or second_before_first)
