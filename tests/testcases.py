'''
Created on 2011-09-20

@author: xion
'''
import pyduck
import unittest
from tests.interfaces import SimpleInterfaceByMeta, SimpleInterface


class SimpleClass(object):
    def method(self): pass


class BasicTests(unittest.TestCase):
    
    def test_basic_interface_by_meta(self):
        assert pyduck.implements(SimpleClass(), SimpleInterfaceByMeta)

    def test_basic_interface(self):
        assert pyduck.implements(SimpleClass(), SimpleInterface)

    def test_isinstance_by_meta(self):
        assert isinstance(SimpleClass(), SimpleInterfaceByMeta)
        
    def test_isinstance(self):
        assert isinstance(SimpleClass(), SimpleInterface)



if __name__ == '__main__':
    unittest.main();
