'''
pyduck

@summary: Python implementation of Go-like interfaces for more robust duck typing
@author: Karol Kuczmarski "Xion" 
@license: MIT
'''
from interface import InterfaceMeta, Interface, implements, contains, isinterface
from decorators import Any, expects, returns
from wrappers import enforce
from overloading import overload
