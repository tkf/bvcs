import os
import functools


def ras(converter):
    """
    Decorator to convert returned value of a function/generator.

    It is just a function composition. The following two codes are
    equivalent.

    Using `@ras`::

        @ras(converter)
        def function(args):
            ...

        result = function(args)

    Manually do the same::

        def function(args):
            ...

        result = converter(function(args))

    Example:

    >>> @ras(list)
    ... def f():
    ...     for i in range(3):
    ...         yield i
    ...
    >>> f()  # this gives a list, not an iterator
    [0, 1, 2]

    """
    def wrapper(original):
        @functools.wraps(original)
        def func(*args, **kwds):
            return converter(original(*args, **kwds))
        func.original = original
        return func
    return wrapper


def mkdirp(path):
    if not os.path.isdir(path):
        os.makedirs(path)
