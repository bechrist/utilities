"""Profiling utilities

Copyright (c) 2024-, The University of Texas at Austin

All Rights reserved.
See file COPYRIGHT for details.

This file is part of :code:`bechrist`'s :code:`utilities`. For more information see
https://github.com/bechrist/utilities

:code:`utilities` is free software; you can redistribute it and/or modify it under the
terms of the GNU General Public License (as published by the Free
Software Foundation) version 3.0 dated June 2007.
"""
__authors__ = ['Blake Christierson, UT Austin <bechristierson@utexas.edu>']
__all__ = ['profile_timing', 'init_profile_timing']  

from time import time
import typing as typ

from .stdlib_utils import _Decorator, conditional_decorator

# %%
def profile_timing(func: typ.Callable) -> typ.Callable:
    """Timing decorator to be used for profiling code
    
    :param func: Function/callable to be timed
    :type func: typing.Callable
    
    :return: Timed callable
    :rtype: typing.Callable
    """
    def __decorator(*args: tuple[typ.Any], **kwargs: dict[str, typ.Any]) -> typ.Any:
        t0 = time()
        out = func(*args, **kwargs)
        print(f"Function {func.__name__!r}: {time()-t0:.4f}s")
        return out
    return __decorator


def init_profile_timing(init: bool) -> _Decorator:
    return conditional_decorator(profile_timing, init)