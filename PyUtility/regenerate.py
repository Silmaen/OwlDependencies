#!/usr/bin/env python3
from lib_manager import *


def build_config(lib: Library):
    cmd = F"conan create {lib.path}"
    if lib.is_header_only():
        if run(cmd) != 0:
            log(F"in packaging of header-only: {lib}", levels["error"])
            exit(-666)
    else:
        for config in lib.config:
            if run(F"{cmd} -s build_type {config}") != 0:
                log(F"in BUILD of {lib} config {config}", levels["error"])
                exit(-666)


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--library", "-l", type=str, default="", help="The library to construct (default: all)")
    args = parser.parse_args()

    libs = get_ordered_libs(args.library)
    if len(libs) == 0:
        exit(-666)

    for lib in get_ordered_libs(args.library):
        build_config(lib)


if __name__ == "__main__":
    main()
