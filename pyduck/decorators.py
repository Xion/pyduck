'''
Module with decorators that enhance the functionality of pyduck interfaces.

Created on 2011-09-23

@author: xion
'''
from pyduck.utils import is_function, ArgumentSpec, Any
import functools
import inspect
import itertools



###########################################################
# @expects function decorator            

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
        if not is_function(func):
            raise TypeError, "@expects can only decorate functions"
        
        self._improve_argument_spec(func)
        
        @functools.wraps(func)
        def checked_func(*args, **kwargs):
            self._validate_arguments(args, kwargs)
            return func(*args, **kwargs)
        
        checked_func.__arguments__ = self.arg_spec
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


###########################################################
# @returns function decorator

class ReturnValueDecorator(object):
    ''' @returns decorator which can be applied to functions.
    It performs a check whether function's return value
    matches the interface/type specified in the as decorator's argument.
    
    Example:
    @returns(int)
    def maybe_throws():
        die_roll = random.randint(1, 6)
        return 1 if die_roll > 3 else "foo"
    '''
    def __init__(self, retval_spec):
        self.retval_spec = retval_spec
        
    def __call__(self, func):
        if not is_function(func):
            raise TypeError, "@returns can only decorate functions"

        @functools.wraps(func)
        def checked_func(*args, **kwargs):
            retval = func(*args, **kwargs)
            self._validate_return_value(retval)
            
        checked_func.__returns__ = self.retval_spec
        return checked_func

    def _validate_return_value(self, retval):
        ''' Checks whether the specified return values conforms
        with interface/type that was passed to the decorator. '''
        if not isinstance(retval, self.retval_spec):
            expected_type = self.retval_spec.__name__
            actual_type = type(retval).__name__
            raise TypeError, "Invalid return value: expected %s, got %s (%r)" % (expected_type, actual_type, retval)
        
        
returns = ReturnValueDecorator
