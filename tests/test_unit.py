"""
Unit test
"""

from bvcs.methods.clone import parse_repo_file_lines
from bvcs.utils import ras


@ras(list)
def reposettings_to_lines(reposettings, sep=' '):
    for (path, (vcstype, url)) in reposettings.iteritems():
        yield sep.join([path, vcstype, url])


def check_parse_repo_file_lines(lines, actual):
    assert parse_repo_file_lines(lines) == actual


def test_parse_repo_file_lines():
    simple_setting = dict(hgrepo=('hg', 'a'),
                          gitrepo=('git', 'b'),
                          bzrrepo=('bzr', 'c'))
    simple_lines = reposettings_to_lines(simple_setting)

    yield (check_parse_repo_file_lines, simple_lines, simple_setting)
    yield (check_parse_repo_file_lines, simple_lines + ['\n'], simple_setting)
