"""BVSC command line interface"""


def get_parser(method_list):
    from argparse import ArgumentParser
    parser = ArgumentParser()
    subpersers = parser.add_subparsers()
    for method in method_list:
        method().connect_subparser(subpersers)
    return parser


def run():
    from bvcs.methods import METHOD_LIST
    from bvcs.core import applyargs
    parser = get_parser(METHOD_LIST)
    args = parser.parse_args()
    status = applyargs(**vars(args))
    if status != 0:
        import sys
        sys.exit(status)


if __name__ == '__main__':
    run()
