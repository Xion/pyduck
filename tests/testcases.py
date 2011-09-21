'''
Created on 2011-09-20

@author: xion
'''
from pyduck import implements
from pyduck.method import Method
from tests.interfaces import SimpleInterfaceByMeta, SimpleInterface
import unittest


class SimpleClass(object):
    def method(self): pass


class BasicTests(unittest.TestCase):
    
    def test_basic_interface_by_meta(self):
        self.assertTrue(implements(SimpleClass(), SimpleInterfaceByMeta))

    def test_basic_interface(self):
        self.assertTrue(implements(SimpleClass(), SimpleInterface))

    def test_isinstance_by_meta(self):
        self.assertTrue(isinstance(SimpleClass(), SimpleInterfaceByMeta))
        
    def test_isinstance(self):
        self.assertTrue(isinstance(SimpleClass(), SimpleInterface))
        
        
class MethodObjectTests(unittest.TestCase):
    
    def test_method_of_class(self):
        Method(SimpleClass.method)
        
    def test_method_of_object(self):
        obj = SimpleClass()
        Method(obj.method)
    
    def test_non_method(self):
        x = 1
        self.assertRaises(ValueError, Method, x)
        
    def test_basic_identity(self):
        method_obj = Method(SimpleClass.method)
        assert method_obj.conforms_with(SimpleClass.method)
        
        
class BasicMethodSignatureTests(unittest.TestCase):
    
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
            

if __name__ == '__main__':
    unittest.main();
