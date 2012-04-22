import os

from bvcs.core import BaseRunner, command
from bvcs.utils import ras


def hg_clone(path, url, cwd):
    (ret, stdout) = command(['hg', 'clone', url, path], cwd=cwd)
    return (ret, stdout)


def git_clone(path, url, cwd):
    (ret, stdout) = command(['git', 'clone', url, path], cwd=cwd)
    return (ret, stdout)


def bzr_clone(path, url, cwd):
    (ret, stdout) = command(['bzr', 'branch', url, path], cwd=cwd)
    return (ret, stdout)


@ras(dict)
def parse_repo_file_lines(lines):
    for l in lines:
        l = l.strip()
        if not l:
            continue
        (path, vcstype, url) = l.split(' ', 2)
        yield (path, (vcstype, url))


class Clone(BaseRunner):

    cmdname = 'clone'
    dispatcher = {'hg': hg_clone, 'git': git_clone, 'bzr': bzr_clone}

    def get_arg(self, vcstype, path):
        (func, args, kwds) = super(Clone, self).get_arg(vcstype, path)
        return (func, args + (self.reposettings[path][1], self.cwd), kwds)

    def run(self, path, repo_file, num_proc, exclude, **kwds):
        self.load_reposettings(repo_file)
        if path:
            paths = self.filter_path(path, exclude)
        else:
            paths = list(self.reposettings)
        self.cwd = os.path.dirname(repo_file)
        vcstypes = [self.reposettings[p][0] for p in paths]
        results = self.mapper(vcstypes, paths, num_proc)
        return self.reporter(vcstypes, paths, results, **kwds)

    def load_reposettings(self, repo_file_path):
        with open(repo_file_path) as repo_file:
            self.reposettings = parse_repo_file_lines(repo_file.readlines())

    def reporter(self, vcstypes, paths, results):
        print 'Cloned {0} repositories'.format(len(paths))

    def add_parser(self, parser):
        parser = super(Clone, self).add_parser(parser)
        parser.add_argument('--repo-file', default='.bvcsrepo')
        return parser
