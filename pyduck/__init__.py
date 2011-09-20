import inspect


class InterfaceMeta(type):
    ''' Metaclass for interfaces. '''
    
    def __new__(meta, class_name, bases, class_dict): #@NoSelf
        ''' Creates the new interface. '''
        methods = get_methods(class_dict)
        iface_dict = build_iface_dict(methods)
        
        internals = get_internals(class_dict)
        iface_dict.update(internals)
        
        return type.__new__(meta, class_name, bases, iface_dict)
    
    def __instancecheck__(iface, instance): #@NoSelf
        ''' Custom instance checking. Causes isinstance() to verify interface. '''
        return implements(instance, iface)
        

def get_methods(class_dict):
    return filter(inspect.isfunction, class_dict.itervalues())

def build_iface_dict(methods):
    res = {}    # just names for now
    for m in methods:
        res[m.func_name] = m
    return res

def get_internals(class_dict):
    is_internal = lambda name: name.startswith('__') and name.endswith('__')
    return dict((k, v) for k, v in class_dict.iteritems() if is_internal(k))


###############################################################################


class Interface(object):
    ''' Base class for interfaces. It automatically uses the interface metaclass. '''
    __metaclass__ = InterfaceMeta
    
    
def implements(obj, interface):
    # checking only names of methods now
    for name, method_obj in interface.__dict__.iteritems():
        if name.startswith('_'):   continue
        obj_member = getattr(obj, name, None)
        if not (obj_member and inspect.ismethod(obj_member)):
            return False
        
    return True
