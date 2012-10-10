import os

from bvcs.core import BaseRunner, command


def hg_init(path):
    (ret, stdout) = command(['hg', 'init', path])
    return (ret, stdout)


def git_init(path):
    (ret, stdout) = command(['git', 'init', path])
    return (ret, stdout)


def bzr_init(path):
    (ret, stdout) = command(['bzr', 'init', path])
    return (ret, stdout)


def parse_repo_path(path):
    if path.endswith(os.path.sep):
        path = os.path.dirname(path)
    (repo, vcsdir) = os.path.split(path)
    if not vcsdir.startswith('.'):
        raise ValueError('VCS directory (.hg/.git/.bzr) must start with a dot')
    return (vcsdir[1:], repo)


class Init(BaseRunner):

    """
    Initialize Hg/Git/Bzr repositories.

    Example::

        bvcs init bitbuckt/.hg github/.git launchpad/.bzr

    """

    cmdname = 'init'
    dispatcher = {'hg': hg_init, 'git': git_init, 'bzr': bzr_init}

    def run(self, path, num_proc, exclude, **kwds):
        path = self.filter_path(path, exclude)
        (vcstypes, paths) = zip(*map(parse_repo_path, path))
        self.results = results = self.mapper(vcstypes, paths, num_proc)
        return self.reporter(vcstypes, paths, results, **kwds)

    def reporter(self, vcstypes, paths, results):
        print 'Initialized {0} repositories'.format(len(paths))
