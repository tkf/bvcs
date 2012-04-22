"""
Functional testing
"""

import os
import shutil
from contextlib import contextmanager

from bvcs.utils import ras
from bvcs.methods import init


TESTDIR = os.path.dirname(__file__)


@ras(list)
def genepaths(*args):
    """
    Generate paths

    >>> genepaths('a', 'b', ['1', '2', '3'])
    ['a/b/1', 'a/b/2', 'a/b/3']

    """
    paren = args[:-1]
    lastdirs = args[-1]
    for name in lastdirs:
        dirs = paren + (name,)
        yield os.path.join(*dirs)


def getrepopaths(testname, vcstypes=['hg', 'git', 'bzr']):
    lastdirs = map(os.path.join('{0}repo', '.{0}').format, vcstypes)
    paths = genepaths(TESTDIR, 'functional', testname, lastdirs)
    return paths


@contextmanager
def checkrepos(paths):
    for p in paths:
        shutil.rmtree(os.path.dirname(p), ignore_errors=True)
    yield
    for p in paths:
        assert os.path.isdir(p)


def check_runner(runnerclass, testname):
    paths = getrepopaths(testname)
    runner = runnerclass()
    with checkrepos(paths):
        runner.run(path=paths, num_proc=1, exclude=[])


def test_init():
    check_runner(init.Init, 'init')
