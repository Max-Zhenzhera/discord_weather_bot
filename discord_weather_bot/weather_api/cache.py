"""
Implements functions for caching.

.. func:: cache_key_builder(f, *args, **kwargs) -> str
    Generate key for cache
"""

from __future__ import annotations


def cache_key_builder(f, *args, **kwargs) -> str:
    """ Generate key for cache """
    to_str_and_casefold = lambda var: str(var).casefold()

    parse_func = f.__name__
    parse_args = '-'.join(map(to_str_and_casefold, args))
    parse_kwargs = '-'.join(
        [f'{to_str_and_casefold(key)}:{to_str_and_casefold(value)}' for key, value in kwargs.items()]
    )
    key = '|'.join([parse_func, parse_args, parse_kwargs])

    return key
