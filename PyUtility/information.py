#!/usr/bin/env python3
from lib_manager import *


def local():
    """
    Analyse the local folders for libraries
    """
    libs = get_ordered_libs()
    for lib in libs:
        log(F"{lib}")


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--local", "-l", type=str, default="", help="Check this repository")
    args = parser.parse_args()

    all_actions = ["local"]
    actions = []
    if args.local not in [None, ""]:
        actions.append("local")
    if len(actions) == 0:
        actions = all_actions

    for action in actions:
        if action == "local":
            local()


if __name__ == "__main__":
    main()
