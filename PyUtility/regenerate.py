#!/usr/bin/env python3
from functions import *
from introspection import *


def build_config(where: Path, config: str = ""):
    cmd = F"conan create {where}"
    if config not in ["", None]:
        cmd += F" -s build_type={config}"
    return run(cmd)


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--library", "-l", type=str, default="", help="The libreary to construct (default: all)")
    args = parser.parse_args()

    root = get_root_dir() / "Libs"
    to_do = "all"
    if args.library not in [None, ""]:
        if not (root / args.library ).exists():
            log(F"No library {args.library} found!", levels["error"])
            exit(-666)
        to_do = args.library

    for lib in root.iterdir():
        if to_do not in ["all", lib.name]:
            continue
        if not (lib / "conanfile.py ").exists():
            continue
        if (lib / "configs").exists():
            with open(lib / "configs") as fc:
                lines = [l.strip() for l in fc.readlines()]
        else:
            lines = [""]
        for config in lines:
            if build_config(lib, config) != 0:
                log(F"in BUILD of {lib} config {config}", levels["error"])
                exit(-666)


if __name__ == "__main__":
    main()
