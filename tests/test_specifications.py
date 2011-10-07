'''
Contains tests for code related to checking method
argument and return type specifications,
and interfaces that employ them.

Created on 2011-10-07

@author: xion
'''
from pyduck import implements, expects, returns
from tests.common import TypedArgsInterface, TypedReturnInterface
import unittest

    

class TypedInterfacesTests(unittest.TestCase):
    
    def test_correct_args_class(self):
        class CorrectArgsClass(object):
            @expects(int)
            def method(self, n):    pass
        assert implements(CorrectArgsClass, TypedArgsInterface)
    
    def test_untyped_args_class(self):
        class UntypedArgsClass(object):
            def method(self, n): pass
        self.assertFalse(implements(UntypedArgsClass, TypedArgsInterface))
        
    def test_wrongly_typed_args_class(self):
        class WrongArgTypesClass(object):
            def method(self, n): pass
        self.assertFalse(implements(WrongArgTypesClass, TypedArgsInterface))
        
    def test_correct_return_type(self):
        class CorrectReturnTypeClass(object):
            @returns(int)
            def method(self):   return 1
        assert implements(CorrectReturnTypeClass, TypedReturnInterface)
        
    def test_untyped_return_class(self):
        class UntypedReturnClass(object):
            def method(self):   pass
        self.assertFalse(implements(UntypedReturnClass, TypedReturnInterface))
        
    def test_wrong_return_type(self):
        class WrongReturnTypeClass(object):
            @returns(str)
            def method(self):   return ""
        self.assertFalse(implements(WrongReturnTypeClass, TypedReturnInterface))
