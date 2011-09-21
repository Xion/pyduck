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
        assert implements(SimpleClass(), SimpleInterfaceByMeta)

    def test_basic_interface(self):
        assert implements(SimpleClass(), SimpleInterface)

    def test_isinstance_by_meta(self):
        assert isinstance(SimpleClass(), SimpleInterfaceByMeta)
        
    def test_isinstance(self):
        assert isinstance(SimpleClass(), SimpleInterface)
        
        
class MethodObjectTests(unittest.TestCase):
    
    def test_method_of_class(self):
        Method(SimpleClass.method)
        
    def test_method_of_object(self):
        obj = SimpleClass()
        Method(obj.method)
    
    def test_non_method(self):
        def function(): pass
        self.assertRaises(ValueError, Method, function)
        
    def test_basic_identity(self):
        method_obj = Method(SimpleClass.method)
        assert method_obj.conforms_with(SimpleClass.method)



if __name__ == '__main__':
    unittest.main();
