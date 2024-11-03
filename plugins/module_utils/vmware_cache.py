from __future__ import absolute_import, division, print_function

__metaclass__ = type

import shelve
from datetime import datetime
import os
from dill import Pickler, Unpickler


CACHE_TTL = os.getenv('ANSIBLE_VMWARE_CACHE_TTL', 7)
shelve.Pickler = Pickler
shelve.Unpickler = Unpickler


class VmwareCache():
    def __init__(self):
        self.filename = "/tmp/vmware.vmware"
        try:
            if not self.read('_expiration_time'):
                self.write('_expiration_time', datetime.now().timestamp() + CACHE_TTL)
        except:
            self.write('_expiration_time', datetime.now().timestamp() + CACHE_TTL)

    def reset(self):
        with shelve.open(self.filename, flag='n') as s:
            s['_expiration_time'] = datetime.now().timestamp() + CACHE_TTL

    def exists(self):
        try:
            with shelve.open(self.filename, flag='r'):
                pass
        except Exception:
            return False
        return True

    def write(self, key, val):
        with shelve.open(self.filename, flag='c') as s:
            s[key] = val

    def read(self, key):
        with shelve.open(self.filename, flag='r') as s:
            try:
                if datetime.now().timestamp() > s['_expiration_time']:
                    self.reset()
                    return None
                return s[key]
            except KeyError:
                return None



def cache(func):
    def wrapper(*args, **kwargs):
        cache = VmwareCache()
        cache_key = f"{func.__name__}_{hash_function_inputs(args, kwargs)}"
        cached_result = cache.read(cache_key)
        if cached_result:
            return cached_result
        else:
            res = func(*args, **kwargs)
            cache.write(cache_key, res)
            return res

    return wrapper


def hash_function_inputs(args, kwargs):
    try:
        arg_hash = hash(args)
    except TypeError:
        arg_hash = hash(''.join([str(a) for a in args]))
    return (
        f"{arg_hash}"
        f"{hash(tuple(sorted(kwargs.items())))}"
    )
