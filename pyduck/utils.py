'''
Module with convenience utilities for easier usage of
pyduck interfaces.

Created on 2011-09-23

@author: xion
'''
import functools
import inspect
import itertools


###########################################################
# @expects function decorator

class Any(object):
    ''' Marker symbol used with @expects decorator.
    Accepts any type of Python object. '''
    pass


class ArgumentSpec(dict):
    ''' Slightly customized version of standard Python dictionary
    that stores the argument specification for a function.
    It is a mapping of argument indices and names into pyduck interfaces
    or Python types. It also handles the cases of variadic arguments and
    keywords arguments if needed.
    '''
    def __init__(self, *args, **kwargs):
        super(ArgumentSpec, self).__init__(*args, **kwargs)
        self.allows_varargs = False
        self.allows_kwargs = False
    
    def __getitem__(self, key):
        try:
            return super(ArgumentSpec, self).__getitem__(key)
        except IndexError:
            if isinstance(key, (int, long)):
                if self.allows_varargs: return Any
                raise
            elif isinstance(key, str):
                if self.allows_kwargs:  return Any
                raise
            raise TypeError, "Invalid argument index or name - must be a number or ANSI string"
            
    def __setitem__(self, key, value):
        if not (isinstance(key, (int, long)) or isinstance(key, str)):
            raise TypeError, "Invalid argument index or name - must be a number or ANSI string"
        return super(ArgumentSpec, self).__setitem__(key, value)
            

class ExpectedParametersDecorator(object):
    ''' @expects decorator which can be applied to functions.
    It performs a check whether function's actual parameters
    match the specification (in terms of pyduck interfaces)
    passed to the decorator.
    
    Example:
    @expects(Any, FileLikeObject)
    def write(value, dest_file):
        # ...
    '''
    def __init__(self, *args, **kwargs):
        self.arg_spec = ArgumentSpec()
        for i, arg in enumerate(args):
            self.arg_spec[i] = arg
        self.arg_spec.update(kwargs)
        self.is_method = False  # we can't know it yet
    
    def __call__(self, func):
        is_function = inspect.isfunction(func) or inspect.ismethod(func)
        if not is_function:
            raise TypeError, "@expects can only decorate functions"
        
        self._improve_argument_spec(func)
        
        @functools.wraps(func)
        def checked_func(*args, **kwargs):
            self._validate_arguments(args, kwargs)
            return func(*args, **kwargs)
        
        return checked_func
    
    def _improve_argument_spec(self, func):
        ''' Uses the actual arguments of function to improve
        the argument specification which was saved with the decorator
        object during its creation. The improved version should work
        regardless of how the argument was used (positionally or via keyword)
        in function call.
        '''
        arg_names, varargs_name, kwargs_name, _ = inspect.getargspec(func)
        if len(arg_names) > 0 and arg_names[0] == 'self':
            self.is_method = True
            arg_names = arg_names[1:]   # omit 'self'

        if len(arg_names) > len(self.arg_spec):
            raise TypeError, "Expected a function with %s argument(s), found only %s" % (len(self.arg_spec), len(arg_names))
         
        for i, arg_name in enumerate(arg_names):
            arg_type = self.arg_spec.get(i) or self.arg_spec.get(arg_name)
            self.arg_spec[i] = arg_type
            self.arg_spec[arg_name] = arg_type
            
        if varargs_name:    self.arg_spec.allows_varargs = True
        if kwargs_name:     self.arg_spec.allows_kwargs = True
        
    def _validate_arguments(self, varargs, kwargs):
        ''' Checks whether specified arguments of function conform with
        the specification which was passed earlier to the decorator. '''
        if self.is_method:
            varargs = varargs[1:]   # omit 'self'
            
        all_args = itertools.chain(enumerate(varargs), kwargs.iteritems())
        for key, arg in all_args:
            expected = self.arg_spec[key]
            if expected is Any: continue
            if not isinstance(arg, expected):
                expected_type = expected.__name__
                actual_type = type(arg).__name__
                raise TypeError, "Invalid argument: expected %s, got %s (%r)" % (expected_type, actual_type, arg)
            

expects = ExpectedParametersDecorator
