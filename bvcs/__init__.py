# [[[cog import cog
#    cog.outl('"""\n%s\n"""' % file('../README-header.rst').read())
# ]]]
"""
Batched VCS commands
====================

Run bunch of VCS commands (git/hg/bzr) over a set of repositories.

Use cases:

* You want to make sure you pushed changes to remote for all of your
  repositories.
* You want to log the revision of all of your repositories.
* You are using git but want to have hg/bzr repositories as submodule.
* You want to do (equivalent of) ``git fetch`` for all of your repositories.
* etc...

"""
# [[[end]]]

__author__ = "Takafumi Arakaki"
__version__ = "0.0.1.dev0"
__license__ = "MIT License"
