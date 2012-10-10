import sys
import subprocess

import bvcs.methods
import bvcs.core


def generate_readme(out=sys.stdout):
    newline = lambda: out.write("\n")

    with open("README-header.rst") as f:
        out.writelines(f.readlines())
    newline()

    for method in bvcs.core.RUNNER.keys():
        title = '``bvcs {}``'.format(method)
        underline = '-' * len(title)
        newline()
        out.write(title)
        newline()
        out.write(underline)
        newline()
        newline()
        out.write(
            subprocess.check_output(
                ['python', '-m', 'bvcs.cli', method, '--help']))
        newline()


if __name__ == '__main__':
    generate_readme()
