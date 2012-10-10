from bvcs.core import BaseRunner, command


def isclean_from_stdout(stdout):
    unclean = stdout.strip().splitlines()
    if unclean:
        return (False, '{0} unclean files'.format(len(unclean)))
    else:
        return (True, 'clean')


def hg_isclean(path):
    (ret, stdout) = command(['hg', 'status'], cwd=path)
    return isclean_from_stdout(stdout)


def git_isclean(path):
    (ret, stdout) = command(['git', 'status', '--short'], cwd=path)
    return isclean_from_stdout(stdout)


def bzr_isclean(path):
    (ret, stdout) = command(['bzr', 'status', '--short'], cwd=path)
    return isclean_from_stdout(stdout)


class IsClean(BaseRunner):

    """
    Test if the working directory of all repositories are clean or not.

    This command runs one of the following commands in each repository::

        hg status
        git status --short
        bzr status --short

    """

    cmdname = 'isclean'
    dispatcher = {'hg': hg_isclean, 'git': git_isclean, 'bzr': bzr_isclean}

    def reporter(self, vcstypes, paths, results):
        allclean = True
        for (vcstype, name, (clean, msg)) in zip(vcstypes, paths, results):
            if not clean:
                allclean = False
                print "{0} ({1}): {2}".format(name, vcstype, msg)
        return allclean
