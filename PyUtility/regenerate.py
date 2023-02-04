#!/usr/bin/env python3
from lib_manager import *


def build_config(where: Path, config: str = ""):
    cmd = F"conan create {where}"
    if config not in ["", None]:
        cmd += F" -s build_type={config}"
    return run(cmd)


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--library", "-l", type=str, default="", help="The library to construct (default: all)")
    args = parser.parse_args()

    libs = get_ordered_libs(args.library)
    if len(libs) == 0:
        exit(-666)

    for lib in get_ordered_libs(args.library):
        if lib.is_header_only():
            if build_config(lib, "") != 0:
                log(F"in packaging of header-only: {lib}", levels["error"])
                exit(-666)
        else:
            for config in lib.config:
                if build_config(lib, config) != 0:
                    log(F"in BUILD of {lib} config {config}", levels["error"])
                    exit(-666)


if __name__ == "__main__":
    main()
