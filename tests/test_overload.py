'''
Contains tests for the overload() routine.

Created on 2011-10-10

@author: xion
'''
from pyduck import expects, overload
from tests.common import SimpleInterface, SimpleClass
import unittest


@expects(basestring)
def __str_func(arg):
    return str

@expects(int)
def __int_func(arg):
    return int

@expects(SimpleInterface)
def __iface_func(arg):
    return SimpleClass

func = overload(__str_func, __int_func, __iface_func)


class OverloadTests(unittest.TestCase):
    
    def test_global_functions(self):
        assert func("str") == str
        assert func(1) == int
        assert func(SimpleClass()) == SimpleClass

    def test_local_functions(self):
        @expects(basestring)
        def __str_func(arg):
            return str
        @expects(int)
        def __int_func(arg):
            return int
        @expects(SimpleInterface)
        def __iface_func(arg):
            return SimpleClass
        func = overload(__str_func, __int_func, __iface_func)
        
        assert func("str") == str
        assert func(1) == int
        assert func(SimpleClass()) == SimpleClass
        
    def test_methods(self):
        class Class(object):
            @expects(basestring)
            def __str_func(self, arg):
                return str
            @expects(int)
            def __int_func(self, arg):
                return int
            @expects(SimpleInterface)
            def __iface_func(self, arg):
                return SimpleClass
            func = overload(__str_func, __int_func, __iface_func)
            
        obj = Class()
        assert obj.func("str") == str
        assert obj.func(1) == int
        assert obj.func(SimpleClass()) == SimpleClass
