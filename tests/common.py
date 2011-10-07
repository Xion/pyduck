'''
Common code shared by many testcases.

Created on 2011-10-07

@author: xion
'''
from pyduck import InterfaceMeta, Interface, expects, returns


class SimpleInterfaceByMeta(object):
    __metaclass__ = InterfaceMeta
    def method(self): pass
    
class SimpleInterface(Interface):
    def method(self): pass


class SimpleClass(object):
    def method(self): pass


class TypedArgsInterface(Interface):    
    @expects(int)
    def method(self, n):    pass
    
class TypedReturnInterface(Interface):
    @returns(int)
    def method(self):   pass
