"""Python standard library utilities

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
__all__ = ['_Decorator', 'conditional_decorator',
           'igetattr', 
           'str2num']

import typing as typ

# %%
_Decorator = typ.Callable[[typ.Callable], typ.Callable]


def conditional_decorator(dec: _Decorator, cond: bool) -> typ.Callable:
    """Conditional decorator

    :param dec: Decorator
    :type dec: _Decorator

    :param cond: Conditional boolean
    :type cond: bool

    :return: Conditional decorator
    :rtype: typing.Callable
    """
    def __decorator(func):
        return dec(func) if cond else func
    return __decorator


# %%
def igetattr(obj: object, attr: str) -> typ.Any:
    """Retrieves case insensitive object attribute

    :param obj: Object 
    :type obj: object

    :param attr: Attribute name
    :type attr: str

    :return: Attribute
    :rtype: typing.Any
    """
    for a in dir(obj):
        if a.lower() == attr.lower():
            return getattr(obj, a)
        

# %%
def str2num(s: str) -> int | float | str:
    """Will convert string to integer or float if possible

    :param s: String to parse
    :type s: str

    :return: Parsed value
    :rtype: int | float | str
    """
    s2 = s.replace(',', '')
    try: 
        return int(s2)
    except:
        pass

    try:
        return float(s2)
    except:
        return s