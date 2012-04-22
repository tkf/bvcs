"""
Functional testing
"""

import os
import shutil
from contextlib import contextmanager

from bvcs.utils import ras
from bvcs.methods import init, clone


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


def check_runner(runner, testname, path=None, num_proc=1, exclude=[], **kwds):
    testpaths = getrepopaths(testname)
    with checkrepos(testpaths):
        path = testpaths if path is None else path
        runner.run(path=path, num_proc=num_proc, exclude=exclude, **kwds)


def test_init():
    check_runner(init.Init(), 'init')


def test_clone():
    test_init()
    testname = 'clone'
    repo_file = os.path.join(TESTDIR, 'functional', testname, '.bvcsrepo')
    check_runner(clone.Clone(), testname, path=[], repo_file=repo_file)
