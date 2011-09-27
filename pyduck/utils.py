'''
Module with auxiliary code used throughout the library.

Created on 2011-09-27

@author: xion
'''
import inspect
import sys


def is_function(func):
    ''' Generalized check for methods and normal functions. '''
    return inspect.ismethod(func) or inspect.isfunction(func)


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
