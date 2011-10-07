'''
Contains tests for the @returns decorator.

Created on 2011-10-07

@author: xion
'''
from pyduck import returns, expects, Any
from tests.common import SimpleClass, SimpleInterface
import unittest



def function_returning_None():
    pass
def function_returning_int():
    return 1
def function_returning_string():
    return "foo"
def function_returning_simpleclass():
    return SimpleClass     
        
        
class ReturnsDecoratorTests(unittest.TestCase):
    
    def _functions_for_tests(self):
        return [function_returning_None, function_returning_int,
                function_returning_string, function_returning_simpleclass] 
    
    def test_non_function(self):
        decorator = returns(Any)
        self.assertRaises(TypeError, decorator, 1)
        
    def test_any(self):
        decorator = returns(Any)
        for func in self._functions_for_tests():
            decorated = decorator(func)
            decorated()
            
    def test_int(self):
        decorator = returns(int)
        decorator(function_returning_int)()
        self.assertRaises(TypeError, decorator(function_returning_None))
        self.assertRaises(TypeError, decorator(function_returning_string))
        self.assertRaises(TypeError, decorator(function_returning_simpleclass))
        
    def test_string(self):
        decorator = returns(str)
        decorator(function_returning_string)()
        self.assertRaises(TypeError, decorator(function_returning_None))
        self.assertRaises(TypeError, decorator(function_returning_int))
        self.assertRaises(TypeError, decorator(function_returning_simpleclass))
        
    def test_correct_iface(self):
        decorator = returns(SimpleInterface)
        decorator(function_returning_simpleclass)()
        
    def test_incorrect_iface(self):
        decorator = returns(SimpleInterface)
        class OtherClass(object):
            def method(self, a, b): pass
        func = lambda: OtherClass()
        self.assertRaises(TypeError, decorator(func))
        
    def test_expects_and_returns(self):
        @expects(int, str)
        @returns(str)
        def fun1(a, s): return str(a) + s
        @returns(str)
        @expects(int)
        def fun2(i):    return str(i)
        self.assertRaises(TypeError, fun1, 1, 1)
        self.assertRaises(TypeError, fun2, "foo")
        fun1(1, "foo")
        fun2(1)
