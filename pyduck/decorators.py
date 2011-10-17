'''
Module with decorators that enhance the functionality of pyduck interfaces.

Created on 2011-09-23

@author: xion
'''
from pyduck.utils import ArgumentSpec, Any
import functools
import inspect
import itertools


def transfer_specs(from_func, to_func):
    ''' Utility function that transfers the specifications
    from one (decorated) function to another. Used by @expects
    and @returns decorators.
    '''
    spec_attrs = ['_arguments', '_has_self', '_returns']
    
    attrs = filter(lambda a: hasattr(from_func, a), spec_attrs)
    for attr in attrs:
        from_func_value = getattr(from_func, attr)
        setattr(to_func, attr, from_func_value)
        
    return to_func


###########################################################
# @expects function decorator

class ArgumentError(TypeError):
    ''' Exception raised when arguments passed to function
    do not agree with specification given to @expects decorator. '''
    def __init__(self, message, argument = None, expected = None):
        super(ArgumentError, self).__init__(message)
        self.argument = argument
        self.expected = expected

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
        self.omit_self = False  # we don't know yet what function we'll decorate
    
    def __call__(self, func):
        if not inspect.isroutine(func):
            raise TypeError, "@expects can only decorate functions"
        
        self._improve_argument_spec(func)
        
        @functools.wraps(func)
        def checked_func(*args, **kwargs):
            self._validate_arguments(args, kwargs)
            return func(*args, **kwargs)
        
        checked_func = transfer_specs(func, checked_func)
        checked_func._arguments = self.arg_spec
        checked_func._has_self = self.omit_self
        return checked_func
    
    def _improve_argument_spec(self, func):
        ''' Uses the actual arguments of function to improve
        the argument specification which was saved with the decorator
        object during its creation. The improved version should work
        regardless of how the argument was used (positionally or via keyword)
        in function call.
        '''
        arg_names, varargs_name, kwargs_name, _ = inspect.getargspec(func)
        
        first_arg_is_self = len(arg_names) > 0 and arg_names[0] == 'self'
        is_unbound_method = not inspect.ismethod(func) and first_arg_is_self
        if is_unbound_method:
            self.omit_self = True
        if first_arg_is_self:
            arg_names = arg_names[1:]   # 'self' is not part of argument spec

        if len(arg_names) > len(self.arg_spec):
            raise TypeError("Expected a function with %s argument(s), found only %s"
                            % (len(self.arg_spec), len(arg_names)))
         
        for i, arg_name in enumerate(arg_names):
            arg_type = self.arg_spec.get(i) or self.arg_spec.get(arg_name)
            self.arg_spec[i] = arg_type
            self.arg_spec[arg_name] = arg_type
            
        if varargs_name:    self.arg_spec.allows_varargs = True
        if kwargs_name:     self.arg_spec.allows_kwargs = True
        
    def _validate_arguments(self, varargs, kwargs):
        ''' Checks whether specified arguments of function conform with
        the specification which was passed earlier to the decorator. '''
        if self.omit_self:
            varargs = varargs[1:]   # omit 'self'
            
        all_args = itertools.chain(enumerate(varargs), kwargs.iteritems())
        for key, arg in all_args:
            expected = self.arg_spec[key]
            if expected is Any: continue
            if not self._is(arg, expected):
                expected_type = expected.__name__
                actual_type = type(arg).__name__
                raise ArgumentError("Invalid argument: expected %s, got %s (%r)" % (expected_type, actual_type, arg),
                                    argument = arg, expected = expected)
            
    @staticmethod
    def _is(obj, type_):
        ''' Generalized functions for checking whether an object
        is an instance of given type. It supports all necessary pyduck features
        that are relevant here, such as boolean predicates. '''
        # TODO: add support for boolean predicates
        return isinstance(obj, type_)
            

expects = ExpectedParametersDecorator


###########################################################
# @returns function decorator

class ReturnValueError(TypeError):
    ''' Exception raised when value returned by function
    does not agree with specification given to @returns decorator. '''
    def __init__(self, message, returned = None, expected = None):
        super(ReturnValueError, self).__init__(message)
        self.returned = returned
        self.expected = expected

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
        if not inspect.isroutine(func):
            raise TypeError, "@returns can only decorate functions"

        @functools.wraps(func)
        def checked_func(*args, **kwargs):
            retval = func(*args, **kwargs)
            self._validate_return_value(retval)
            
        checked_func = transfer_specs(func, checked_func)
        checked_func._returns = self.retval_spec
        return checked_func

    def _validate_return_value(self, retval):
        ''' Checks whether the specified return values conforms
        with interface/type that was passed to the decorator. '''
        if not isinstance(retval, self.retval_spec):
            expected_type = self.retval_spec.__name__
            actual_type = type(retval).__name__
            raise ReturnValueError("Invalid return value: expected %s, got %s (%r)" % (expected_type, actual_type, retval),
                                   returned = retval, expected = self.retval_spec)
        
        
returns = ReturnValueDecorator
