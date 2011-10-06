'''
Contains the Method class, which represents a method of an interface
whose existence and signature is being checked against.

Created on 2011-09-21

@author: xion
'''
from pyduck.utils import Interval, is_function
import inspect


class Method(object):
    ''' Represents the method of an interface. '''

    def __init__(self, actual_method):
        ''' Initializes the object from an actual method. '''
        if not is_function(actual_method):
            raise ValueError, "Expected method/function, got %r" % actual_method
        
        arg_desc = inspect.getargspec(actual_method)
        arg_names, varargs_name, kwargs_name, default_values = arg_desc
        default_values = default_values or []
        
        self.name = actual_method.func_name
        self.has_varargs = varargs_name is not None
        self.has_kwargs = kwargs_name is not None
        self._arguments = getattr(actual_method, '_arguments', None)  # present if @expects was used
        self._returns = getattr(actual_method, '_returns', None)    # present if @returns was used
        
        fixed_arglist = not (self.has_varargs or self.has_kwargs)
        self.max_args = len(arg_names) if fixed_arglist else None
        self.min_args = len(arg_names) - len(default_values)
        
    def is_checked(self):
        ''' Returns True if the method's arguments or return value are checked
        against a specification. This happens if @expects or @returns decorators are used. '''
        return self._arguments is not None or self._returns is not None
        
    def conforms_with(self, method):
        ''' Checks whether given method is compatible with method signature
        described by this very object.
        @note: This relation is NOT symmetrical if optional arguments (incl.
        *args and **kwargs) are concerned. '''
        if isinstance(method, Method):
            method_obj = method
        elif inspect.ismethod(method):
            method_obj = Method(method)
        else:
            raise ValueError, "Expected a method, got %r" % method

        # check number of arguments
        self_arg_range = Interval(self.min_args, self.max_args)
        other_arg_range = Interval(method_obj.min_args, method_obj.max_args)
        if not other_arg_range.contains(self_arg_range):
            return False
        
        # check if other method allows additional args that we don't permit
        if method_obj.has_varargs and not self.has_varargs:
            return False
        if method_obj.has_kwargs and not self.has_kwargs:
            return False
        
        # check if argument specifications match (if they are used)
        if self._arguments:
            if not method_obj._arguments:    return False
            if not self._arguments.conforms_with(method_obj._arguments):
                return False
            
        # check if return types match (if they were specified)
        if self._returns:
            if not method_obj._returns:  return False
            if not issubclass(method_obj._returns, self._returns):
                return False
        
        return True
