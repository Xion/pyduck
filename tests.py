
'''
Created on 2011-09-20

@author: xion
'''
from pyduck import implements, Interface, InterfaceMeta, expects, Any
from pyduck.decorators import returns
from pyduck.method import Method
import unittest


class SimpleInterfaceByMeta(object):
    __metaclass__ = InterfaceMeta
    def method(self): pass
    
class SimpleInterface(Interface):
    def method(self): pass
    
class OptArgInterface(Interface):
    def method(self, arg = 0): pass


class SimpleClass(object):
    def method(self): pass


class BasicInstanceTests(unittest.TestCase):
    
    def test_basic_interface_by_meta(self):
        self.assertTrue(implements(SimpleClass(), SimpleInterfaceByMeta))

    def test_basic_interface(self):
        self.assertTrue(implements(SimpleClass(), SimpleInterface))

    def test_isinstance_by_meta(self):
        self.assertTrue(isinstance(SimpleClass(), SimpleInterfaceByMeta))
        
    def test_isinstance(self):
        self.assertTrue(isinstance(SimpleClass(), SimpleInterface))
        

class BasicClassTests(unittest.TestCase):
    
    def test_basic_interface_by_meta(self):
        self.assertTrue(implements(SimpleClass, SimpleInterfaceByMeta))
        
    def test_basic_interface(self):
        self.assertTrue(implements(SimpleClass, SimpleInterface))

    def test_isinstance_by_meta(self):
        self.assertTrue(isinstance(SimpleClass, SimpleInterfaceByMeta))
        
    def test_isinstance(self):
        self.assertTrue(isinstance(SimpleClass, SimpleInterface))
        
        
class AdvancedInterfaceTests(unittest.TestCase):
    
    def test_optarg_iface_vs_arg_class(self):
        class SimpleClassWithArg(object):
            def method(self, arg): pass
        self.assertFalse(implements(SimpleClassWithArg, OptArgInterface))
        
    def test_optarg_iface_vs_noarg_class(self):
        self.assertFalse(implements(SimpleClass, OptArgInterface))
        
    def test_optarg_iface_vs_optarg_class(self):
        class SimpleClassWithOptArg(object):
            def method(self, arg = 1): pass
        assert implements(SimpleClassWithOptArg, OptArgInterface)
        
        
class MethodObjectTests(unittest.TestCase):
    
    def test_method_of_class(self):
        Method(SimpleClass.method)
        
    def test_method_of_object(self):
        obj = SimpleClass()
        Method(obj.method)
    
    def test_non_method(self):
        self.assertRaises(ValueError, Method, 1)
        
    def test_basic_identity(self):
        method_obj = Method(SimpleClass.method)
        self.assertTrue(method_obj.conforms_with(SimpleClass.method))
        
        
class MethodSignatureTests(unittest.TestCase):
    
    def test_optional_args(self):
        class SimpleClassWithOptionalArgs(object):
            def method(self, a = 0): pass
        self.assertTrue(isinstance(SimpleClassWithOptionalArgs, SimpleInterface))
        
    def test_varagrs(self):
        class SimpleInterfaceWithVarargs(Interface):
            def method(self, *args): pass
        self.assertFalse(isinstance(SimpleClass(), SimpleInterfaceWithVarargs))
    
    def test_too_many_arguments(self):
        class SimpleClassWithTooManyArgs(object):
            def method(self, a): pass
        self.assertFalse(isinstance(SimpleClassWithTooManyArgs, SimpleInterface))

    def test_unwanted_varagrs(self):
        class SimpleClassWithVarargs(object):
            def method(self, *args): pass
        self.assertFalse(isinstance(SimpleClassWithVarargs, SimpleInterface))

    def test_unwanted_kwargs(self):
        class SimpleClassWithKwargs(object):
            def method(self, **kwargs): pass
        self.assertFalse(isinstance(SimpleClassWithKwargs, SimpleInterface))
        
    
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
            

if __name__ == '__main__':
    unittest.main();
