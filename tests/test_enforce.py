'''
Contains tests for the enforce() wrapper.

Created on 2011-10-07

@author: xion
'''
from pyduck import enforce
from tests.common import TypedArgsInterface, TypedReturnInterface
import unittest


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
