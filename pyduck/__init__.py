'''
pyduck

@summary: Utility framework for easier & more robust duck typing in Python
@author: Karol Kuczmarski "Xion" 
@license: MIT
'''
from interface import InterfaceMeta, Interface, implements, contains, isinterface
from decorators import ExamineArgumentsDecorator, Any, expects, returns
from wrappers import enforce
from overloading import overload
