'''
Contains tests for the @expects decorator.

Created on 2011-10-07

@author: xion
'''
from pyduck import expects, Any
from tests.common import SimpleInterface, SimpleClass
import unittest



def normal_function(first, second):
    pass
def variadic_function(arg, *args):
    pass
def keyword_function(arg1, arg2, **kwargs):
    pass
def flexible_function(arg, *args, **kwargs):
    pass
        
        
class ExpectsDecoratorTests(unittest.TestCase):
    
    def test_non_function(self):
        decorator = expects(Any)
        self.assertRaises(TypeError, decorator, 1)
    
    def test_any(self):
        decorator = expects(Any, Any)
        decorated = decorator(normal_function)
        decorated(1, [{'foo':42}])
        
    def test_too_short_argspec(self):
        decorator = expects(Any)
        self.assertRaises(TypeError, decorator, normal_function)
        
    def test_correct_iface_arg(self):
        decorator = expects(SimpleInterface, Any)
        decorated = decorator(normal_function)
        decorated(SimpleClass(), 1)
        
    def test_incorrect_iface_arg(self):
        decorator = expects(SimpleInterface, Any)
        decorated = decorator(normal_function)
        self.assertRaises(TypeError, decorated, (1, 0))
        
    def test_keyword_args(self):
        decorator = expects(first = SimpleInterface, second = SimpleInterface)
        decorated = decorator(normal_function)
        decorated(first = SimpleClass(), second = SimpleClass())
        
    def test_normal_spec_but_keyword_call(self):
        decorator = expects(SimpleInterface, Any)
        decorated = decorator(normal_function)
        decorated(first = SimpleClass(), second = "")
        
    def test_keyword_spec_but_normal_call(self):
        decorator = expects(Any, second = SimpleInterface)
        decorated = decorator(normal_function)
        decorated(1, SimpleClass())
        
    def test_function_with_variadic_args(self):
        decorator = expects(Any, SimpleInterface)
        decorated = decorator(variadic_function)
        decorated(1, SimpleClass())
        self.assertRaises(TypeError, decorated, 0, 1)
        
    def test_function_with_keyword_args(self):
        decorator = expects(Any, Any, foo = SimpleInterface)
        decorated = decorator(keyword_function)
        decorated(0, 1, foo = SimpleClass())
        self.assertRaises(TypeError, decorated, 0, 1, foo = 2)
        
    def test_decorated_method(self):
        class SomeClass(object):
            @expects(SimpleInterface, SimpleInterface)
            def method(self, a, b): pass
        obj = SomeClass()
        obj.method(SimpleClass(), SimpleClass())
        self.assertRaises(TypeError, obj.method, 1, SimpleClass())
        self.assertRaises(TypeError, obj.method, SimpleClass(), 1)
        
    def test_decorated_method_without_self(self):
        ''' This test illustrates the fact that @expects relies on the strong
        Python convention for first method argument to be named 'self',
        In fact, this is how it tells apart methods from regular functions.
        (There is no other way since decorator is applied before a class
        is even created, and methods-to-be are plain functions at this time).
        '''
        class SomeClass(object):
            @expects(SimpleInterface)
            def method(arg): pass #@NoSelf
        obj = SomeClass()
        self.assertRaises(TypeError, obj.method, SimpleClass())
