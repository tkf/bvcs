from bvcs.core import BaseRunner, command


def hg_pull(path):
    return command(['hg', 'pull'], cwd=path)


def git_pull(path):
    return command(['git', 'fetch'], cwd=path)


class Pull(BaseRunner):

    cmdname = 'pull'
    dispatcher = {'hg': hg_pull, 'git': git_pull}

    def reporter(self, vcstypes, paths, results):
        for ((ret, stdout), path, vcstype) in zip(results, paths, vcstypes):
            if ret != 0:
                print '{0} ({1})'.format(path, vcstype)
                print stdout
