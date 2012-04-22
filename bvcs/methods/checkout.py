from bvcs.core import BaseRunner, command


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
        ['bzr', 'checkout', '--revision', state], cwd=path)
    return (ret, stdout)


class Checkout(BaseRunner):

    cmdname = 'checkout'
    dispatcher = {'hg': hg_checkout, 'git': git_checkout, 'bzr': bzr_checkout}

    def get_arg(self, vcstype, path):
        (func, args, kwds) = super(Checkout, self).get_arg(vcstype, path)
        return (func, args + (self.states[path],), kwds)

    def run(self, state_file, **kwds):
        self.load_states(state_file)
        return super(Checkout, self).run(**kwds)

    def load_states(self, state_file):
        self.states = states = {}
        with open(state_file) as state:
            states.update(reversed(l.strip().split(' ', 1))
                          for l in state.readlines())

    def reporter(self, vcstypes, paths, results):
        print 'Checked out {0} repositories'.format(len(paths))

    def add_parser(self, parser):
        parser = super(Checkout, self).add_parser(parser)
        parser.add_argument('--state-file', default='.bvcsstate')
        return parser
