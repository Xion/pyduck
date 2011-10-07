'''
Contains tests for the Method class.

Created on 2011-10-07

@author: xion
'''
from pyduck.method import Method
from tests.common import SimpleClass
import unittest


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
