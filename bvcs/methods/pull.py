from bvcs.core import BaseRunner, command


def hg_pull(path):
    return command(['hg', 'pull'], cwd=path)


def git_pull(path):
    return command(['git', 'fetch'], cwd=path)


def bzr_pull(path):
    # TODO: implement!
    return True


class Pull(BaseRunner):

    """
    Pull changes from remote server (but don't change the local branch).

    It runs one of the following commands in each repositories::

        hg pull
        git fetch

    .. warning:: bzr command is not implemented yet!

    """

    cmdname = 'pull'
    dispatcher = {'hg': hg_pull, 'git': git_pull, 'bzr': bzr_pull}

    def reporter(self, vcstypes, paths, results):
        for ((ret, stdout), path, vcstype) in zip(results, paths, vcstypes):
            if ret != 0:
                print '{0} ({1})'.format(path, vcstype)
                print stdout
