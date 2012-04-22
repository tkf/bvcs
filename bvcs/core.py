import os
import re
import subprocess

from bvcs.utils import ras


def apply3(a):
    # Note: function called via multiprocessing.Pool must be defined
    # as a top level function.  Therefore, this function cannot be in
    # a class (not even as a static method) nor dynamically created.
    (func, args, kwds) = a
    return func(*args, **kwds)


def getpoolmap(num_proc):
    """
    Get Pool.map function with the given number of processes

    If the number of processes is one, the standard map function
    will be returned.

    """
    if num_proc > 1:
        from multiprocessing import Pool
        pool = Pool(processes=num_proc)
        return pool.map
    else:
        return map


@ras(list)
def get_vcs_repos(pathlist):
    for path in pathlist:
        for subpath in os.listdir(path):
            if subpath == '.hg':
                yield ('hg', path)
                break
            elif subpath == '.git':
                yield ('git', path)
                break
            elif subpath == '.bzr':
                yield ('bzr', path)
                break


def joinre(regexs):
    return "|".join(map("({0})".format, regexs))


class ClassRegister(object):

    def __init__(self, key):

        class ClassRegisterMetaClass(type):
            def __init__(cls, name, bases, dict):
                super(ClassRegisterMetaClass, cls).__init__(name, bases, dict)
                val = getattr(cls, key, None)
                if val is not None:
                    registry.append((val, cls))

        self.registry = registry = []
        self.metaclass = ClassRegisterMetaClass

    def classes(self):
        return [c for (n, c) in self.registry]


RUNNER = ClassRegister('cmdname')


class BaseRunner(object):

    __metaclass__ = RUNNER.metaclass

    dispatcher = None
    """A dictionary to map VCS name (hg/git/bzr) to pickle-able function."""

    cmdname = None
    """A string to indicate sub command name."""

    def __init__(self):
        self._check_dispatcher()

    def _check_dispatcher(self):
        import pickle
        try:
            pickle.dumps(list(self.dispatcher.itervalues()))
        except pickle.PicklingError:
            raise ValueError(
                'Functions in {0}.dispatcher must be pickle-able.'
                .format(self.__class__.__name__))

    @staticmethod
    def filter_path(path, exclude):
        if exclude:
            match_exclue = re.compile(joinre(exclude)).match
        else:
            match_exclue = lambda x: False
        return filter(lambda x: not match_exclue(x), path)

    def run(self, path, num_proc, exclude, **kwds):
        repos = get_vcs_repos(self.filter_path(path, exclude))
        (vcstypes, paths) = zip(*repos)
        results = self.mapper(vcstypes, paths, num_proc)
        return self.reporter(vcstypes, paths, results, **kwds)

    def get_arg(self, vcstype, path):
        return (self.dispatcher[vcstype], (path,), {})

    def mapper(self, vcstypes, paths, num_proc):
        poolmap = getpoolmap(len(vcstypes) if num_proc == 0 else num_proc)
        args = map(self.get_arg, vcstypes, paths)
        return poolmap(apply3, args)

    def reporter(self, vcstype, path, result):
        raise NotImplementedError

    def connect_subparser(self, subpersers):
        return self.add_parser(subpersers.add_parser(self.cmdname))

    def add_parser(self, parser):
        parser.add_argument(
            '-p', '--num-proc', metavar='N', type=int, default=1,
            help='number of processes to use. '
            '0 means use as much as possible. (default: %(default)s)')
        parser.add_argument(
            '-X', '--exclude', default=[], action='append',
            help='paths to exclude as regular expression. '
            'this option can be given multiple times.')
        parser.add_argument(
            'path', nargs='+',
            help='search for VCS repositories under these directories')
        parser.set_defaults(func=self.run)  # used via `applyargs`
        return parser


def applyargs(func, **kwds):
    return func(**kwds)


def command(cmds, *args, **kwds):
    cmds = list(a for a in cmds if a)  # exclude empty string
    proc = subprocess.Popen(
        cmds, *args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kwds)
    ret = proc.wait()
    return (ret, proc.stdout.read())
