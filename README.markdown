pyduck
=

_pyduck_ is a Python utility framework for effective use of **duck typing** - one of the core concepts
driving the language. It aims to solve some issues which naturally arise when using try-and-fail approach
to interfacing with objects.

Rationale
-
As an example, consider the following code:

    try:
        some_object.perform_first_operation()
        some_object.perform_second_operation()
    except AttributeError:
        logging.error("Object %r cannot perform both operations", some_object)
    except Exception:
        logging.exception("Error occured")

Here <code>some_object</code> has been received from the outside and two operations are being executed on it
without checking whether relevant method are actually available. Since possible exceptions are being caught
(particularly the <code>AttributeError</code>), this doesn't seem to be a problem in most cases.
If, however, there is a possibility for <code>some_object</code> to support first operation and not second,
executing <code>perform_first_operation</code> might commit some irreversible actions that leave the system
in inconsistent state. To prevent that, we would usually need some form of transactions which the above
code will be executed in. This would not be the case if we could check whether <code>some_object</code>
supports both operations we are requesting.

Overview
-
_pyduck_ provides means for easy verifying whether a particular object supports operations we want to
perform on it **before** actually attempting them. It does so not by polling for any explicitly declared
types (<code>isinstance</code>/<code>issubclass</code>) but by checking if object implements a particular
**interface**.
