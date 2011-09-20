'''
Created on 2011-09-20

@author: xion
'''
import pyduck


class SimpleInterfaceByMeta(object):
    __metaclass__ = pyduck.InterfaceMeta
    def method(self): pass
    
class SimpleInterface(pyduck.Interface):
    def method(self): pass


class ReadableFileLike(object):
    __metaclass__ = pyduck.InterfaceMeta
    def read(self): pass
