'''
Module with convenience utilities for easier usage of
pyduck interfaces.

Created on 2011-09-23

@author: xion
'''
import inspect
import functools


###########################################################
# @expects function decorator

class Any(object):
    ''' Marker symbol used with @expects decorator.
    Accepts any type of Python object. '''
    pass


# Note: currently the check this decorator performs is simple
# and does not recognize cases where positional arguments
# (positional wrt to how they interfaces were passed to @expects)
# has been passed through keywords in the actual function call.
# This shall be fixed.

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
        self.varargs_spec = args
        self.kwargs_spec = kwargs
    
    def __call__(self, func):
        is_function = inspect.isfunction(func) or inspect.ismethod(func)
        if not is_function:
            raise TypeError, "@expects can only decorate functions"
        
        @functools.wraps(func)
        def checked_func(*args, **kwargs):
            self._check_params_conformance(args, kwargs)
            return func(*args, **kwargs)
        
        return checked_func
        
    def _check_params_conformance(self, varargs, kwargs):
        ''' Checks whether specified arguments of function
        conform with the specification which was passed earlier to the decorator. '''
        try:
            for i in xrange(min(len(self.varargs_spec), len(varargs))):
                actual, expected = varargs[i], self.varargs_spec[i]
                if expected is Any: continue
                if not isinstance(actual, expected):
                    raise TypeError(actual, expected)
                
            for k in kwargs:
                actual, expected = kwargs[k], self.kwargs_spec[k]
                if expected is Any: continue
                if not isinstance(actual, expected):
                    raise TypeError(actual, expected)
        except TypeError, e:
            actual, expected = e.args
            exc_dict = {
                        'e_type': expected.__name__,
                        'a_type': type(actual).__name__,
                        'a_value': actual,
                        }
            raise TypeError, "Invalid parameter: expected '%(e_type)s', got '%(a_type)s' (%(a_value)r)" % exc_dict
        

expects = ExpectedParametersDecorator
