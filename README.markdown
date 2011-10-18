# Easier & more robust duck typing

**pyduck** is a Python utility framework for more effective usage of language's defining traits: _duck typing_.
It enhances the language with several useful features that increase the readability and reliability of Python code.

```python
from pyduck import Interface, expects, Any, overload

class Iterable(Interface):
    def __iter__(self): pass

@expects(Iterable)
def __iterable_as_json(value):
    json_list = map(as_json, value)
    return "[%s]" % str.join(",", json_list)

@expects(basestring)
def __string_as_json(value):
    return '"%s"' % str(value)

@expects(Any)
def __other_as_json(value):
    return str(value)

as_json = overload(__iterable_as_json, __string_as_json, __other_as_json)
```

Features
-
* **interfaces** which do not need to be explicitly declared (similar to Go language)
* automatic **interface/type checking** for function arguments
* **function overloading** based on interfaces/types of arguments
* automatic interface/type checking for function return values

For more info & the docs, see the [project's webpage](http://xion.github.com/pyduck).
