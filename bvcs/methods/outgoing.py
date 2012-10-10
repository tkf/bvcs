from bvcs.core import BaseRunner, command


def hg_out(path):
    (ret, stdout) = command(['hg', 'outgoing'], cwd=path)
    out = ret == 0
    return (out, stdout)


def hg_out_cached(path):
    (ret, stdout) = command(['hg', 'cout'], cwd=path)
    out = ret == 0
    return (out, stdout)


def hg_out_phase(path):
    (ret, stdout) = command(
        ['hg', 'log', '--rev', 'draft()', '--template',
         r'{node|short} {desc|firstline}\n'], cwd=path)
    out = bool(stdout.strip())
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


def hg_apropos_out_command():
    (_unused_, hghelp) = command(['hg', 'help'])
    if 'phase' in hghelp:
        return hg_out_phase
    elif 'cout' in hghelp:
        return hg_out_cached
    else:
        return hg_out


def get_shortpath():
    try:
        from uniquify import shortpath
        return shortpath
    except ImportError:
        return lambda x: x


class Outgoing(BaseRunner):

    """
    Check if you have something to push.

    This command does not communicate with remote server.  It checks
    if the state of the remote branch remembered by the local
    repository and compares it to the current state of the local
    branch.  If the local branch has something new, this commands
    report that you have something to push.

    """

    cmdname = 'outgoing'
    dispatcher = {'hg': hg_out, 'git': git_out, 'bzr': bzr_out}

    def __init__(self):
        self.dispatcher = self.dispatcher.copy()
        self.dispatcher['hg'] = hg_apropos_out_command()
        super(Outgoing, self).__init__()

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
