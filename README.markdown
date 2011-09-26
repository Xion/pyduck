# pyduck

_pyduck_ is a Python utility framework for effective use of **duck typing** - one of the core concepts
driving the language. It aims to solve some issues which naturally arise when using try-and-fail approach
to interfacing with objects.

Rationale
-
As an example, consider the following code:

```python
try:
    some_object.perform_first_operation()
    some_object.perform_second_operation()
except AttributeError:
    logging.error("Object %r cannot perform both operations", some_object)
except Exception:
    logging.exception("Error occured")
```

Here <code>some\_object</code> has been received from the outside and two operations are being executed on it
without checking whether relevant method are actually available. Since possible exceptions are being caught
(particularly the <code>AttributeError</code>), this doesn't seem to be a problem in most cases.
If, however, there is a possibility for <code>some\_object</code> to support first operation and not second,
executing <code>perform\_first\_operation</code> might commit some irreversible changes that leave the system
in inconsistent state. To prevent that, we would usually need some form of transactions which the above
code will be executed in. This would not be the case if we could check whether <code>some\_object</code>
supports both operations we are requesting.

Overview
-
_pyduck_ provides means for easy verifying whether a particular object supports operations we want to
perform on it **before** actually attempting them. It does so not by polling for any explicitly declared
"markers" (such as standard Python superclasses, or [abstract base classes][abc] registered using
<code>ABCMeta.register</code>) but by checking if object implements a particular **interface**.

An interface is simply a specification of methods an object should have in order to be considered as
an implementation of that interface. The important note is that object does _not_ need to explicitly
declare that it implements an interface - it only needs to actually have those particular methods.

This is somewhat similar to the interface model used by the Go language. The bottom line is that 
_no interface has to be explictly declared_ - or even known about! - by the implementor.

[abc]: http://docs.python.org/library/abc.html

Installation
-
A (relatively) stable release should be available from [PyPi][pypi]:

    $ sudo easy_install pyduck

If you prefer to use the latest revision, clone the Git repo and install the package in development mode:

    $ git clone git://github.com/Xion/pyduck.git
    $ cd pyduck
    $ sudo ./setup.py develop

This allows to <code>git pull</code> changes without having to run <code>setup.py</code> again.  

[pypi]: http://pypi.python.org/pypi/pyduck/

Examples
-
Consider the canonical pythonic example of duck typing: the file-like object. If we expect to receive
such object and use its <code>read</code>, we can define an interface for it:

```python
import pyduck

class ReadableFileLike(pyduck.Interface):
    def read(self): pass
```

It can then be used to verify whether particular object satisfies our conditions:

```python
def load(file_obj):
    if not pyduck.implements(file_obj, ReadableFileLike):
        raise TypeError, "Readable file-like object expected"
    # ...
```

Of course this particular example isn't very impressive as it's essentially a wrapped <code>hasattr</code>
call. But we could define a more strict specification that also enforces a particular method signature:

```python
class Parser(pyduck.Interface):
    def load(self, file_obj): pass
    def dump(self, data, file_obj, **kwargs): pass

def serialize_data(parser):
    if pyduck.implements(parser, Parser):
        file_obj = open("file.dat", "w")
        parser.dump(data, file_obj, whitespace=False)

def deserialize_data(parser):
    if pyduck.implements(parser, Parser):
        file_obj = open("file.dat")
        data = parser.load(file_obj)
```

_pyduck_ is capable of checking the number of arguments, their kind (normal, variadic, keyword) and whether
they are optional or not.
