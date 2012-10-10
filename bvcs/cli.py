"""BVSC command line interface"""


def get_parser(method_list):
    from argparse import ArgumentParser
    parser = ArgumentParser(
        prog='bvcs',
    )
    subpersers = parser.add_subparsers()
    for method in method_list:
        method().connect_subparser(subpersers)
    return parser


def run():
    import bvcs.methods  # this will register runners
    from bvcs.core import applyargs, RUNNER
    parser = get_parser(RUNNER.classes())
    args = parser.parse_args()
    status = applyargs(**vars(args))
    if status != 0:
        import sys
        sys.exit(status)


if __name__ == '__main__':
    run()
