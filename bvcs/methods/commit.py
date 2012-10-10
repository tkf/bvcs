from bvcs.core import BaseRunner, command


def hg_commit(path, message):
    (ret, stdout) = command(
        ['hg', 'commit', '--addremove', '--message', message], cwd=path)
    return (ret, stdout)


def git_commit(path, message):
    (ret, stdout) = command(['git', 'add', '.'], cwd=path)
    if ret != 0:
        return (ret, stdout)
    (ret, stdout) = command(['git', 'ls-files', '--deleted'], cwd=path)
    if ret != 0:
        return (ret, stdout)
    deleted = stdout.splitlines()
    if deleted:
        (ret, stdout) = command(['git', 'rm'] + deleted, cwd=path)
        if ret != 0:
            return (ret, stdout)
    (ret, stdout) = command(
        ['git', 'commit', '--message', message], cwd=path)
    return (ret, stdout)


def bzr_commit(path, message):
    (ret, stdout) = command(['bzr', 'add'], cwd=path)
    if ret != 0:
        return (ret, stdout)
    (ret, stdout) = command(['bzr', 'remove'], cwd=path)
    if ret != 0:
        return (ret, stdout)
    (ret, stdout) = command(
        ['bzr', 'commit', '--message', message], cwd=path)
    return (ret, stdout)


class Commit(BaseRunner):

    """
    Commit the current working directories.

    It runs one of the following commands in each repositories.

    For Mercurial repositoreis

        hg commit --addremove --message MESSAGE

    For Git repositoreis::

        git add .
        git rm DELETE_FILES  # if needed
        git commit --message MESSAGE

    For Bzr repositoreis::

        bzr add
        bzr remove
        bzr commit --message MESSAGE

    """

    cmdname = 'commit'
    dispatcher = {'hg': hg_commit, 'git': git_commit, 'bzr': bzr_commit}

    def get_arg(self, vcstype, path):
        (func, args, kwds) = super(Commit, self).get_arg(vcstype, path)
        return (func, args + (self.message,), kwds)

    def run(self, message, **kwds):
        self.message = message
        return super(Commit, self).run(**kwds)

    def reporter(self, vcstypes, paths, results):
        print 'Performed commit on {0} repositories'.format(len(paths))

    def add_parser(self, parser):
        parser = super(Commit, self).add_parser(parser)
        parser.add_argument(
            '--message', default='Auto-commit by BVCS',
            help='Commit message (same for all repositories).')
        return parser
