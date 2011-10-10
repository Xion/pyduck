'''
Contains tests for the enforce() wrapper.

Created on 2011-10-07

@author: xion
'''
from pyduck import Interface, expects, enforce
from tests.common import TypedArgsInterface, TypedReturnInterface
import unittest


class TypedTwoArgsInterface(Interface):
    @expects(int, basestring)
    def method(self, an_int, a_string):
        pass


class EnforceTests(unittest.TestCase):
    
    def test_enforced_expects(self):
        class Class(object):
            def method(self, n):
                self.n = n
        obj = Class()
        wrapped_obj = enforce(TypedArgsInterface).on(obj)
        wrapped_obj.method(1)
        assert wrapped_obj.n == 1
        self.assertRaises(TypeError, wrapped_obj.method, "foo")
        
    def test_enforced_expects_with_2args(self):
        class Class(object):
            def method(self, n, s):
                self.n = n
                self.s = s
        obj = Class()
        wrapped_obj = enforce(TypedTwoArgsInterface).on(obj)
        wrapped_obj.method(1, "bar")
        assert wrapped_obj.n == 1 and wrapped_obj.s == "bar"
        self.assertRaises(TypeError, wrapped_obj.method, "foo", 1)
        
    def test_enforced_returns_on_correct_object(self):
        class Class(object):
            def method(self):
                return 1
        obj = Class()
        wrapped_obj = enforce(TypedReturnInterface).on(obj)
        wrapped_obj.method()
        
    def test_enforced_returns_on_incorrect_object(self):
        class Class(object):
            def method(self):
                return "foo"
        obj = Class()
        wrapped_obj = enforce(TypedReturnInterface).on(obj)
        self.assertRaises(TypeError, wrapped_obj.method)
        
    def test_enforce_syntax(self):
        class Class(object):
            def method(self):
                return 1
            
        wrapped_obj = enforce(TypedReturnInterface).on(Class())
        wrapped_obj.method()
        wrapped_obj = enforce(TypedReturnInterface)(Class())
        wrapped_obj.method()
        wrapped_obj = enforce(TypedReturnInterface, Class())
        wrapped_obj.method()
        
        obj = Class() ; enforce(TypedReturnInterface).on(obj)
        obj.method()
        obj = Class() ; enforce(TypedReturnInterface)(obj)
        obj.method()
        obj = Class() ; enforce(TypedReturnInterface, obj)
        obj.method()
