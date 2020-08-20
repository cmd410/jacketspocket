"""Implementing switchcase as context manager
"""
from typing import Sequence


def throw(exc):
    """Raise exceptions from lambdas
    """
    raise exc


class FoundBranch(Exception): 
    """Exception to exit context early
    """
    pass


class Switch:

    __slots__ = ('test_case',
                 'is_type',
                 'default',
                 'args',
                 'kwargs',
                 'branches')

    def __init__(self, test_case, *args, **kwargs):
        self.test_case = test_case
        self.is_type = isinstance(self.test_case, type)
        self.args = args
        self.kwargs = kwargs
        self.branches = []
        self.default = None

    def check_case(self, case, is_case_type):
        if not (is_case_type or isinstance(case, SwitchType)):
            return self.test_case == case
        else:
            if self.is_type:
                return issubclass(self.test_case, case)
            else:
                return isinstance(self.test_case, case)

    def __enter__(self):
        def case(in_case, branch=None):

            is_case_type = isinstance(in_case, type)

            is_case_default = issubclass(in_case, Default) \
                              if is_case_type \
                              else isinstance(in_case, Default)
            if not is_case_default:
                is_the_case = self.check_case(in_case, is_case_type)
            else:
                is_the_case = False
            
            if branch is None:
                # Work as decorator
                def decorator(func):
                    if is_the_case:
                        self.branches.append(func)
                        raise FoundBranch
                    elif is_case_default:
                        self.default = func
                    return func
                return decorator
            
            if is_the_case:
                self.branches.append(branch)
                raise FoundBranch
            elif is_case_default:
                self.default = branch
        return case
    
    def __exit__(self, exc_type, exc_val, traceback):
        if self.branches:
            self.branches[0](*self.args, **self.kwargs)
        elif self.default:
            self.default(*self.args, **self.kwargs)
        if exc_type == FoundBranch:
            return True


class SwitchType:
    __slots__ = ()


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

        def collect_len(l, limit=0):
            if not limit:
                return []
            length = [len(l)]
            child_len = []
            for i in l:
                if isinstance(i, Sequence):
                    child_len.extend(collect_len(i, limit-1))
            
            if child_len:
                length.append(sum(child_len)//len(child_len))
            return length
        
        lengths = collect_len(instance, len(self.shape))

        for l, s in zip(lengths, self.shape):
            if l != s:
                return False
        return True
    
    def __subclasscheck__(self, subclass):
        return issubclass(subclass, self.cls)
