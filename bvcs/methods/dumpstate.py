from bvcs.core import BaseRunner, command
from bvcs.methods.identify import bzr_id


def hg_dump_state(path):
    (ret, stdout) = command(
        ['hg', 'log', '--rev', '.', '--template', '{node}'], cwd=path)
    return stdout.strip()


def git_dump_state(path):
    (ret, stdout) = command(
        ['git', 'log', '--pretty=format:%H', '-n1'], cwd=path)
    return stdout.splitlines()[0]


class DumpState(BaseRunner):

    cmdname = 'dump'
    dispatcher = {'hg': hg_dump_state, 'git': git_dump_state, 'bzr': bzr_id}

    def reporter(self, vcstypes, paths, results, state_file):
        with open(state_file, 'w') as out:
            out.writelines(map('{0} {1}\n'.format, results, paths))

    def add_parser(self, parser):
        parser = super(DumpState, self).add_parser(parser)
        parser.add_argument('--state-file', default='.bvcsstate')
        return parser
