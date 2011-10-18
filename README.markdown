# Easier & more robust duck typing

**pyduck** is a Python utility framework for more effective usage of language's defining traits: _duck typing_.
It enhances the language with several useful features that increase the readability and reliability of Python code.

```python
from pyduck import Interface, expects, overload

class Iterable(Interface):
    def __iter__(self): pass

@expects(basestring)
def __string_as_json(value):
    return '"%s"' % str(value)

@expects(Iterable)
def __iterable_as_json(value):
    json_list = map(as_json, value)
    return "[%s]" % str.join(",", json_list)

as_json = overload(__string_as_json, __iterable_as_json)
```

