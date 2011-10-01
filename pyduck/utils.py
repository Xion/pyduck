'''
Module with auxiliary code used throughout the library.

Created on 2011-09-27

@author: xion
'''
import inspect
import sys


class Any(object):
    ''' Marker symbol used with argument specifications.
    Accepts any type of Python object. '''
    class __metaclass__(type):
        def __instancecheck__(cls, other): #@NoSelf
            return True
        

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
    
    def conforms_with(self, arg_spec):
        ''' Checks whether this argument specification conforms with the other one.
        Conformance means that the set of calls that the other spec permits is no bigger
        (in terms of inclusion) than the set calls permitted by this spec. '''
        if not isinstance(arg_spec, ArgumentSpec):
            raise TypeError, "Expected argument spec, got %s (%r)" % (type(arg_spec).__name__, arg_spec)
        
        if self.allows_varargs and not arg_spec.allows_varargs: return False
        if self.allows_kwargs and not arg_spec.allows_kwargs:   return False
        
        arg_names = filter(lambda n: isinstance(n, basestring), arg_spec.keys())
        for arg_name in arg_names:
            if arg_name.startswith('_'):    continue
            self_arg_type = self.get(arg_name)
            if self_arg_type is None:   return False
            other_arg_type = arg_spec.get(arg_name)
            if not issubclass(other_arg_type, self_arg_type):
                return False
            
        return True
    
    
def is_function(func):
    ''' Generalized check for methods and normal functions. '''
    return inspect.ismethod(func) or inspect.isfunction(func)

###########################################################

class Interval(object):
    ''' Represents a numeric interval, closed at either side. '''
    PLUS_INFINITY = sys.maxint
    MINUS_INFINITY = -sys.maxint
    
    def __init__(self, begin = None, end = None):
        self.begin = begin if begin is not None else Interval.MINUS_INFINITY
        self.end = end if end is not None else Interval.PLUS_INFINITY
        if not (self.begin <= self.end):
            raise ValueError, "Invalid interval: %s" % self
        
    def overlaps(self, other):
        ''' Checks whether this interval and the other one overlap. '''
        self_before_other = self.end < other.begin
        other_before_self = other.end < self.begin
        return not (self_before_other or other_before_self)
    
    def contains(self, other):
        ''' Checks whether this interval contains the other one. '''
        return self.begin <= other.begin <= other.end <= self.end 
    
    def is_subset_of(self, other):
        ''' Checks whether this interval is a subset of the other one. '''
        return other.contains(self)

    def __str__(self):
        return "[%s; %s]" % (self.begin, self.end)
