from bvcs.core import BaseRunnerWithState, command
from bvcs.methods.identify import bzr_id


def hg_dump_state(path):
    (ret, stdout) = command(
        ['hg', 'log', '--rev', '.', '--template', '{node}'], cwd=path)
    return stdout.strip()


def git_dump_state(path):
    (ret, stdout) = command(
        ['git', 'log', '--pretty=format:%H', '-n1'], cwd=path)
    return stdout.splitlines()[0]


class DumpState(BaseRunnerWithState):

    cmdname = 'dump'
    dispatcher = {'hg': hg_dump_state, 'git': git_dump_state, 'bzr': bzr_id}

    def reporter(self, vcstypes, paths, results, state_file):
        self.dump_states(state_file, paths, results)
