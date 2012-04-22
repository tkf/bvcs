"""
Functional testing
"""

import os
import shutil
import tempfile

from bvcs.utils import ras, mkdirp
from bvcs.methods import init, clone, commit


TESTDIR = os.path.dirname(__file__)
TESTTEMPDIR = os.path.join(TESTDIR, 'tmp')
mkdirp(TESTTEMPDIR)


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


class CheckFunctionBase(object):

    vcstypes = ['hg', 'git', 'bzr']

    @classmethod
    def name(cls):
        return cls.__name__

    def setUp(self, tmpdir=None):
        if tmpdir is None:
            self.tmpdir = tempfile.mkdtemp(dir=TESTTEMPDIR)
        else:
            self.tmpdir = tmpdir
        self.basedir = os.path.join(self.tmpdir, self.name())
        mkdirp(self.basedir)
        lastdirs = map('{0}repo'.format, self.vcstypes)
        self.paths = genepaths(self.basedir, lastdirs)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def set_paths(self):
        pass

    def make_runner(self):
        raise NotImplemented

    def run_kwds(self):
        kwds = dict(path=self.paths, num_proc=1, exclude=[])
        return self.modify_run_kwds(kwds)

    def modify_run_kwds(self, kwds):
        return kwds

    def test(self):
        runner = self.make_runner()
        runner.run(**self.run_kwds())
        for p in self.paths:
            assert os.path.isdir(p)


class TestInit(CheckFunctionBase):

    make_runner = init.Init

    def modify_run_kwds(self, kwds):
        kwds['path'] = map(
            os.path.join, self.paths, map('.{0}'.format, self.vcstypes))
        return kwds


class CheckFunctionWithInitBase(CheckFunctionBase):

    use_same_basedir = False

    def setUp(self):
        super(CheckFunctionWithInitBase, self).setUp()
        self.init = TestInit()
        self.init.setUp(tmpdir=self.tmpdir)
        self.init.test()
        if self.use_same_basedir:
            self.basedir = self.init.basedir
            self.paths = self.init.paths

    def tearDown(self):
        super(CheckFunctionWithInitBase, self).tearDown()
        self.init.tearDown()


class TestClone(CheckFunctionWithInitBase):

    make_runner = clone.Clone

    def make_repo_file(self):
        repo_file = os.path.join(self.basedir, '.bvcsrepo')
        file(repo_file, 'w').write(
            "hgrepo hg {0}\n"
            "gitrepo git {1}\n"
            "bzrrepo bzr {2}\n"
            .format(*map(os.path.abspath, self.init.paths)))
        return repo_file

    def modify_run_kwds(self, kwds):
        kwds.update(path=[], repo_file=self.make_repo_file())
        return kwds


class TestCommit(CheckFunctionWithInitBase):

    use_same_basedir = True
    make_runner = commit.Commit

    def make_some_change(self):
        for p in self.paths:
            with open(os.path.join(p, 'README.txt'), 'w') as f:
                f.write('This is a dummy file.')

    def test(self):
        self.make_some_change()
        super(TestCommit, self).test()

    def modify_run_kwds(self, kwds):
        kwds['message'] = 'Commit message.'
        return kwds
