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


``bvcs outgoing``
-----------------

usage: bvcs outgoing [-h] [-p N] [-X EXCLUDE] [path [path ...]]

Check if you have something to push.

This command does not communicate with remote server.  It checks
if the state of the remote branch remembered by the local
repository and compares it to the current state of the local
branch.  If the local branch has something new, this commands
report that you have something to push.

positional arguments:
  path                  search for VCS repositories under these directories

optional arguments:
  -h, --help            show this help message and exit
  -p N, --num-proc N    number of processes to use. 0 means use as much as
                        possible. (default: 1)
  -X EXCLUDE, --exclude EXCLUDE
                        paths to exclude as regular expression. this option
                        can be given multiple times.


``bvcs identify``
-----------------

usage: bvcs identify [-h] [-p N] [-X EXCLUDE] [path [path ...]]

Print human-friendly revision specifier for each repository.

This command runs one of the following commands::

    hg id --num --id --branch --tags --bookmarks
    git show --format=short
    bzr version-info --custom --template {revision_id}

Use `dump` command to save revision of each repository in
program-friendly format.

positional arguments:
  path                  search for VCS repositories under these directories

optional arguments:
  -h, --help            show this help message and exit
  -p N, --num-proc N    number of processes to use. 0 means use as much as
                        possible. (default: 1)
  -X EXCLUDE, --exclude EXCLUDE
                        paths to exclude as regular expression. this option
                        can be given multiple times.


``bvcs pull``
-------------

usage: bvcs pull [-h] [-p N] [-X EXCLUDE] [path [path ...]]

Pull changes from remote server (but don't change the local branch).

It runs one of the following commands in each repositories::

    hg pull
    git fetch

.. warning:: bzr command is not implemented yet!

positional arguments:
  path                  search for VCS repositories under these directories

optional arguments:
  -h, --help            show this help message and exit
  -p N, --num-proc N    number of processes to use. 0 means use as much as
                        possible. (default: 1)
  -X EXCLUDE, --exclude EXCLUDE
                        paths to exclude as regular expression. this option
                        can be given multiple times.


``bvcs dump``
-------------

usage: bvcs dump [-h] [-p N] [-X EXCLUDE] [--state-file STATE_FILE]
                 [path [path ...]]

Dump state (revision id) of the repositories in a file.

The state is saved in the file ``.bvcsstate`` in the current
directory.  This file can be specified explicitly by the
`--state-file` option.  Use `checkout` command to restore
the state stored in the file.

positional arguments:
  path                  search for VCS repositories under these directories

optional arguments:
  -h, --help            show this help message and exit
  -p N, --num-proc N    number of processes to use. 0 means use as much as
                        possible. (default: 1)
  -X EXCLUDE, --exclude EXCLUDE
                        paths to exclude as regular expression. this option
                        can be given multiple times.
  --state-file STATE_FILE
                        File to dump/load states (default: .bvcsstate)


``bvcs checkout``
-----------------

usage: bvcs checkout [-h] [-p N] [-X EXCLUDE] [--state-file STATE_FILE]
                     [path [path ...]]

Run checkout/update for each repository.

Checkout to the state saved in the ``.bvcsstate`` file in the
current This file can be specified explicitly by the
`--state-file` option.  Use `dump` command to save the state
(i.e., "freeze") of the current repositories.

positional arguments:
  path                  search for VCS repositories under these directories

optional arguments:
  -h, --help            show this help message and exit
  -p N, --num-proc N    number of processes to use. 0 means use as much as
                        possible. (default: 1)
  -X EXCLUDE, --exclude EXCLUDE
                        paths to exclude as regular expression. this option
                        can be given multiple times.
  --state-file STATE_FILE
                        File to dump/load states (default: .bvcsstate)


``bvcs init``
-------------

usage: bvcs init [-h] [-p N] [-X EXCLUDE] [path [path ...]]

Initialize Hg/Git/Bzr repositories.

Example::

    bvcs init bitbuckt/.hg github/.git launchpad/.bzr

positional arguments:
  path                  search for VCS repositories under these directories

optional arguments:
  -h, --help            show this help message and exit
  -p N, --num-proc N    number of processes to use. 0 means use as much as
                        possible. (default: 1)
  -X EXCLUDE, --exclude EXCLUDE
                        paths to exclude as regular expression. this option
                        can be given multiple times.


``bvcs clone``
--------------

usage: bvcs clone [-h] [-p N] [-X EXCLUDE] [--repo-file REPO_FILE]
                  [path [path ...]]

Clone repositories given a list of repositories to pull.

The list of repositories are given by ``.bvcsrepo`` file at
current directory.  You can specify it by ``--repo-file`` option.
``.bvcsrepo`` file must follow the following format::

    REPO_PATH REPO_TYPE REPO_URL

For example::

    subrepos/bvcs     git   git://github.com/tkf/bvcs.git
    subrepos/buildlet git   git://github.com/tkf/buildlet.git
    subrepos/cout     hg  https://bitbucket.org/tkf/hgcachedoutgoing

positional arguments:
  path                  search for VCS repositories under these directories

optional arguments:
  -h, --help            show this help message and exit
  -p N, --num-proc N    number of processes to use. 0 means use as much as
                        possible. (default: 1)
  -X EXCLUDE, --exclude EXCLUDE
                        paths to exclude as regular expression. this option
                        can be given multiple times.
  --repo-file REPO_FILE
                        file to specify repositories to clone.


``bvcs commit``
---------------

usage: bvcs commit [-h] [-p N] [-X EXCLUDE] [--message MESSAGE]
                   [path [path ...]]

Commit the current working directories.

It runs one of the following commands in each repositories.

For Mercurial repositoreis

    hg commit --addremove --message MESSAGE

For Git repositoreis::

    git add .
    git rm DELETE_FILES  # if needed
    git commit --message MESSAGE

For Bzr repositoreis::

    bzr add
    bzr remove
    bzr commit --message MESSAGE

positional arguments:
  path                  search for VCS repositories under these directories

optional arguments:
  -h, --help            show this help message and exit
  -p N, --num-proc N    number of processes to use. 0 means use as much as
                        possible. (default: 1)
  -X EXCLUDE, --exclude EXCLUDE
                        paths to exclude as regular expression. this option
                        can be given multiple times.
  --message MESSAGE     Commit message (same for all repositories).


``bvcs isclean``
----------------

usage: bvcs isclean [-h] [-p N] [-X EXCLUDE] [path [path ...]]

Test if the working directory of all repositories are clean or not.

This command runs one of the following commands in each repository::

    hg status
    git status --short
    bzr status --short

positional arguments:
  path                  search for VCS repositories under these directories

optional arguments:
  -h, --help            show this help message and exit
  -p N, --num-proc N    number of processes to use. 0 means use as much as
                        possible. (default: 1)
  -X EXCLUDE, --exclude EXCLUDE
                        paths to exclude as regular expression. this option
                        can be given multiple times.


``bvcs attip``
--------------

usage: bvcs attip [-h] [-p N] [-X EXCLUDE] [path [path ...]]

Print a list of repository which is not at tip of the branch.

This means that you pullled some changes from remote repository
but not yet updated the local branch.

.. warning:: bzr command is not implemented yet!

positional arguments:
  path                  search for VCS repositories under these directories

optional arguments:
  -h, --help            show this help message and exit
  -p N, --num-proc N    number of processes to use. 0 means use as much as
                        possible. (default: 1)
  -X EXCLUDE, --exclude EXCLUDE
                        paths to exclude as regular expression. this option
                        can be given multiple times.

