from bvcs.core import BaseRunner, command


def hg_attip(path):
    (ret1, stdout1) = command(['hg', 'identify', '--id'], cwd=path)
    (ret2, stdout2) = command(['hg', 'identify', '--id', '--rev', 'tip'],
                              cwd=path)
    return stdout1.strip() == stdout2.strip()


def git_attip(path):
    (ret, stdout) = command(['git', 'branch', '-v'], cwd=path)
    for line in stdout.splitlines():
        line = line.lstrip()
        if line.startswith('*'):
            return '[behind' not in line
    return False


def bzr_attip(path):
    # TODO: implement!
    return True


def get_shortpath():
    try:
        from uniquify import shortpath
        return shortpath
    except ImportError:
        return lambda x: x


class AtTip(BaseRunner):

    """
    Print a list of repository which is not at tip of the branch.

    This means that you pullled some changes from remote repository
    but not yet updated the local branch.

    .. warning:: bzr command is not implemented yet!

    """

    cmdname = 'attip'
    dispatcher = {'hg': hg_attip, 'git': git_attip, 'bzr': bzr_attip}

    def reporter(self, vcstypes, paths, results):
        names = get_shortpath()(paths)
        num = 0
        names_not_attip = []
        for (vcstype, path, isattip, name) in zip(
                vcstypes, paths, results, names):
            if not isattip:
                print "{1} [{0}] is not at tip".format(vcstype, name)
                num += 1
                names_not_attip.append(name)
        print "{0}/{1} repositories are waiting to be checked out: {2}".format(
            num, len(paths), ', '.join(names_not_attip))
        return 1 if num > 0 else 0
