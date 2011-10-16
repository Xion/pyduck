'''
Module that contains code for the overloading mechanism
based on @expects declarations.

Created on 2011-10-10

@author: xion
'''
from pyduck.decorators import ExpectedParametersDecorator, ArgumentError
from pyduck.utils import ArgumentSpec
import inspect



def overload(first, *rest):
    ''' Constructs overloaded function using  specified callables.
    Function parts should have an argument specification attached
    by previous application of @expects decorator.
    '''
    if not first:
        raise ValueError, "No functions passed to overload()"
    
    typed_funcs = __reduce_to_function_list([first] + list(rest))
    return __create_overloaded_function(typed_funcs)

    
def __reduce_to_function_list(a_list):
    res = []
    for item in a_list:
        if __is_typed_function(item):
            res.append(item)
        elif hasattr(item, '__iter__'):
            functions_on_list = filter(__is_typed_function, item)
            if len(functions_on_list) < len(item):
                raise TypeError, "List should contain only functions"
            res.extend(item)
        else:
            raise TypeError, "Expected a function or list of functions"
        
    return res
        
def __is_typed_function(arg):
    ''' Utility function that verifies whether given object
    is a "typed function", i.e. either a function with argument
    specification attached or a tuple of function and argument specification.
    '''
    if not arg: return False
    
    if inspect.isroutine(arg):
        arg_spec = getattr(arg, '_arguments', None)
        return isinstance(arg_spec, ArgumentSpec)
    
    if isinstance(arg, tuple):
        return # True -- todo: handle tuples
    
    
def __create_overloaded_function(typed_functions):
    ''' Utility function that creates the overloaded version
    of function that incorporates all the "typed functions"
    specified by the argument.
    '''
    def overloaded_function(*args, **kwargs):
        for func in typed_functions:    # TODO: more intelligent overload resolution
            arg_spec = getattr(func, '_arguments', None)
            if not arg_spec:    continue
            
            # TODO: encapsulate this mechanism inside EPD class
            expects_decorator = ExpectedParametersDecorator()
            expects_decorator.arg_spec = arg_spec
            expects_decorator.omit_self = getattr(func, '_has_self', False)
            try:
                expects_decorator._validate_arguments(args, kwargs)
            except ArgumentError:
                continue
            
            return func(*args, **kwargs)

    return overloaded_function
