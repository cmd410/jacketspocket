"""Implementing switchcase as context manager
"""
from typing import Sequence

from math import floor


def throw(exc):
    """Raise exceptions from lambdas
    """
    raise exc


class Switch:

    __slots__ = ('test_case', 'args', 'kwargs', 'branches')

    def __init__(self, test_case, *args, **kwargs):
        self.test_case = test_case
        self.args = args
        self.kwargs = kwargs
        self.branches = []

    def __enter__(self):
        def case(in_case, branch=None):
            if branch is None:
                # Work as decorator
                def decorator(func):
                    self.branches.append((in_case, func))
                    return func
                return decorator
            
            self.branches.append((in_case, branch))
        return case
    
    def __exit__(self, *_):
        default_branch = None
        for case, branch in self.branches:
            if isinstance(case, Default):
                default_branch = branch
                continue
            elif isinstance(case, type):
                if issubclass(case, Default):
                    default_branch = branch
                    continue
            if isinstance(case, type) or isinstance(case, SwitchType):
                if isinstance(self.test_case, type):

                    if issubclass(self.test_case, case):
                        branch(*self.args, **self.kwargs)
                        break
                else:

                    if isinstance(self.test_case, case):
                        branch(*self.args, **self.kwargs)
                        break
            else:

                if self.test_case == case:
                    branch(*self.args, **self.kwargs)
                    break

        if default_branch:
            default_branch(*self.args, **self.kwargs)


class SwitchType:
    pass


class Default(SwitchType):
    pass


class Shape(SwitchType):

    __slots__ = ('cls', 'shape')

    def __init__(self, cls, *args):
        self.cls = cls
        self.shape = args
    
    def __instancecheck__(self, instance):
        if not isinstance(instance, self.cls):
            return False

        def collect_len(l):
            length = [len(l)]
            child_len = []
            for i in l:
                if isinstance(i, Sequence):
                    child_len.extend(collect_len(i))
            
            if child_len:
                length.append(floor(sum(child_len)/len(child_len)))
            return length
        
        lengths = tuple(collect_len(instance))

        for l, s in zip(lengths, self.shape):
            if l != s:
                return False
        return True
    
    def __subclasscheck__(self, subclass):
        return issubclass(subclass, self.cls)
