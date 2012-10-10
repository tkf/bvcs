from bvcs.core import BaseRunnerWithState, command


def hg_checkout(path, state):
    (ret, stdout) = command(
        ['hg', 'update', '--rev', state], cwd=path)
    return (ret, stdout)


def git_checkout(path, state):
    (ret, stdout) = command(
        ['git', 'checkout', state], cwd=path)
    return (ret, stdout)


def bzr_checkout(path, state):
    (ret, stdout) = command(
        ['bzr', 'update', '--revision', state], cwd=path)
    return (ret, stdout)


class Checkout(BaseRunnerWithState):

    """
    Run checkout/update for each repository.

    Checkout to the state saved in the ``.bvcsstate`` file in the
    current This file can be specified explicitly by the
    `--state-file` option.  Use `dump` command to save the state
    (i.e., "freeze") of the current repositories.

    """

    cmdname = 'checkout'
    dispatcher = {'hg': hg_checkout, 'git': git_checkout, 'bzr': bzr_checkout}

    def get_arg(self, vcstype, path):
        (func, args, kwds) = super(Checkout, self).get_arg(vcstype, path)
        return (func, args + (self.states[path],), kwds)

    def run(self, state_file, **kwds):
        self.load_states(state_file)
        return super(Checkout, self).run(**kwds)

    def reporter(self, vcstypes, paths, results):
        print 'Checked out {0} repositories'.format(len(paths))
