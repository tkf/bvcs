from bvcs.core import BaseRunner, command


def hg_id(path):
    (ret, stdout) = command(
        ['hg', 'id', '--num', '--id', '--branch', '--tags',
         '--bookmarks'], cwd=path)
    return stdout.strip()


def git_id(path):
    (ret, stdout) = command(
        ['git', 'show', '--format=short'], cwd=path)
    return stdout.splitlines()[0]


def bzr_id(path):
    (ret, stdout) = command(
        ['bzr', 'version-info', '--custom', '--template', '{revision_id}'],
        cwd=path)
    return stdout.strip()


class Identify(BaseRunner):

    cmdname = 'identify'
    dispatcher = {'hg': hg_id, 'git': git_id, 'bzr': bzr_id}

    def reporter(self, vcstypes, paths, results):
        for (vcstype, name, rev) in zip(vcstypes, paths, results):
            print "{0} ({1}): {2}".format(name, vcstype, rev)
