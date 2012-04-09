"""BVSC command line interface"""


def get_arg_parser(method_list):
    from argparse import ArgumentParser
    parser = ArgumentParser()
    add_subparsers(parser, method_list)
    return parser


def add_subparsers(parser, method_list):
    subpersers = parser.add_subparsers()
    for method in method_list:
        method().add_subparser(subpersers)


def applyargs(func, **kwds):
    return func(**kwds)


def run():
    from bvcs.methods import METHOD_LIST
    parser = get_arg_parser(METHOD_LIST)
    args = parser.parse_args()
    status = applyargs(**vars(args))
    if status != 0:
        import sys
        sys.exit(status)


if __name__ == '__main__':
    run()
