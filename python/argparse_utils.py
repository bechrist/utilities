""":code:`argparse` utilities

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
__all__ = ['optional', 'validate', 'validate_optional',
           'str2bool', 
           'NestedNamespace', 
           'save_args']

import argparse
import json
import os
import typing as typ


# %%  
# Type Decorators
def optional(cast: typ.Callable[[str], typ.Any]) -> typ.Callable[[str], typ.Any | None]:
    """Decorator for parsing an optional argument

    :param cast: Type casting for argument string
    :type cast: typing.Callable[[str], typing.Any]

    :return: Type casting for optional argument string
    :rtype: typing.Callable[[str], typing.Any | None]
    """
    def __optional(s: str) -> typ.Any | None:
        if (s_ := s.strip()) == 'None':
            return None
        return cast(s_)
    return __optional


def validate(cast: typ.Callable[[str], typ.Any], condition: typ.Callable[[typ.Any], bool]) \
        -> typ.Callable[[str], typ.Any]:
    """Raises :code:`ValueError` if cast value does not meet condition

    :param cast: Type casting for argument string
    :type cast: typing.Callable[[str], typing.Any]

    :param condition: Conditional callable
    :type condition: typing.Callable[[typing.Any], bool]

    :return: Validated type casting for argument string
    :rtype: typing.Callable[[str], typing.Any]
    """
    def __validate(s: str) -> typ.Any:
        value = cast(s.strip())
        if not condition(value):
            raise ValueError(f"Value {value} does not satisfy:{condition}")
        return value
    return __validate


def validate_optional(cast: typ.Callable[[str], typ.Any], condition: typ.Callable[[typ.Any], bool]) \
        -> typ.Callable[[str], typ.Any | None]:
    """Raises :code:`ValueError` if cast optional value does not meet condition

    :param cast: Type casting for argument string
    :type cast: typing.Callable[[str], typing.Any]

    :param condition: Conditional callable
    :type condition: typing.Callable[[typing.Any], bool]

    :return: Validated type casting for optional argument string
    :rtype: typing.Callable[[str], typing.Any | None]
    """
    def __validate_optional(s: str) -> typ.Any | None:
        if (s_ := s.strip()) == 'None':
            return None
        if not condition(v := cast(s_)):
            raise ValueError(f"Value {v} does not satisfy:{condition}")
        return v
    return __validate_optional


# %%
# Type Castings
def str2bool(v: bool | str) -> bool:
    """For desired :code:`argparse` boolean behavior
    
    [1] https://stackoverflow.com/a/43357954
    """
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
    


class NestedNamespace(argparse.Namespace):
    """Allows for hierarchical :code:`argparse` namespaces.
    
    [1] https://stackoverflow.com/questions/18668227/argparse-subcommands-with-nested-namespaces/18709860#18709860
    """
    def __setattr__(self, name, value):
        if '.' in name:
            group, name = name.split('.', 1)
            ns = getattr(self, group, NestedNamespace())
            setattr(ns, name, value)
            self.__dict__[group] = ns
        else:
            self.__dict__[name] = value

    def __getattr__(self, name):
        if '.' in name:
            group, name = name.split('.', 1)
            try:
                ns = self.__dict__[group]
            except KeyError:
                raise AttributeError
            return getattr(ns, name)
        else:
            raise AttributeError


def save_args(args: NestedNamespace, data_dir: os.PathLike):
    """Saves :code:`argparse` arguments to JSON file

    :param args: :code:`argparse` arguments
    :type args: NestedNamespace

    :param data_dir: Directory to save :code:`args.json` to
    :type data_dir: os.PathLike
    """
    def __to_dict(ns: NestedNamespace) -> dict:
        ns_dict = vars(ns).copy()
        for k, v in ns_dict.items():
            if isinstance(v, NestedNamespace):
                ns_dict[k] = __to_dict(v)

        return ns_dict
    
    args_dict = __to_dict(args)
    
    i = 0
    for _ in filter(lambda f: f.startswith('args'), os.listdir(data_dir)):
        i += 1

    file_name = "args.json" if i == 0 else f"args_{i}.json"
    with open(os.path.join(data_dir, file_name), 'w') as file:
        json.dump(args_dict, file)