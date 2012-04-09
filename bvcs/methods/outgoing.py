from bvcs.core import BaseRunner, command


def hg_out(path):
    (ret, stdout) = command(['hg', 'cout'], cwd=path)
    out = ret == 0
    return (out, stdout)


def git_out(path):
    (ret, stdout) = command(['git', 'status'], cwd=path)
    out = ('Your branch is ahead of' in stdout or
           'Changes not staged for commit' in stdout)
    return (out, stdout)


def bzr_out(path):
    (ret, stdout) = command(['bzr', 'missing', '--mine-only'], cwd=path)
    out = 'This branch is up to date.' not in stdout
    return (out, stdout)


def get_shortpath():
    try:
        import uiquify.shortpath
        return uiquify.shortpath
    except ImportError:
        return lambda x: x


class Outgoing(BaseRunner):

    cmdname = 'outgoing'
    dispatcher = {'hg': hg_out, 'git': git_out, 'bzr': bzr_out}

    def reporter(self, vcstypes, paths, results):
        names = get_shortpath()(paths)
        numout = 0
        names_outgoing = []
        for (vcstype, path, (out, stdout), name) in zip(
                vcstypes, paths, results, names):
            if out:
                print "{1} [{0}] needs push!".format(vcstype, name)
                print stdout
                numout += 1
                names_outgoing.append(name)
        print "{0}/{1} repositories are waiting to be pushed: {2}".format(
            numout, len(paths), ', '.join(names_outgoing))
        return 1 if numout > 0 else 0