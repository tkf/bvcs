"""
Functional testing
"""

import os
import shutil

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


def test_init():
    paths = getrepopaths('init')
    for p in paths:
        shutil.rmtree(os.path.dirname(p), ignore_errors=True)
    runner = init.Init()
    runner.run(path=paths, num_proc=1, exclude=[])
    for p in paths:
        assert os.path.isdir(p)
