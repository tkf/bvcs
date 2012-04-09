from setuptools import setup
import bvcs

setup(
    name='bvcs',
    version=bvcs.__version__,
    packages=['bvcs', 'bvcs.methods'],
    description='Asynchronous VCS command runner',
    long_description=bvcs.__doc__,
    author=bvcs.__author__,
    author_email='aka.tkf@gmail.com',
    keywords='vcs, version control system, Git, Mercurial, Bazaar',
    license=bvcs.__license__,
    entry_points={'console_scripts': ['bvcs = bvcs.cli:run']},
    )
