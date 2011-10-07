'''
Contains tests for the core interface functionality:
Interface, InterfaceMeta, etc.

Created on 2011-10-07

@author: xion
'''
from pyduck import implements, contains, Interface
from tests.common import SimpleClass, SimpleInterfaceByMeta, SimpleInterface
import unittest



class OptArgInterface(Interface):
    def method(self, arg = 0): pass
    
class ExtendedInterface(Interface):
    def method(self): pass
    def another_method(self, a): pass
    
class DifferentInterface(Interface):
    def different_method(self): pass



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
        
    def test_contains(self):
        assert contains(SimpleInterface, SimpleInterface)
        assert contains(ExtendedInterface, SimpleInterface)
        assert contains(OptArgInterface, SimpleInterface)
        self.assertFalse(contains(DifferentInterface, SimpleInterface))
        
        
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
