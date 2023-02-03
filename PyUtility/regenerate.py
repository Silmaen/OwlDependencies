#!/usr/bin/env python3
from functions import *
from introspection import *


def build_config(where: Path, config: str = ""):
    cmd = F"conan create {where}"
    if config not in ["", None]:
        cmd += F" -s build_type={config}"
    return run(cmd)


def main():
    import sys
    info = System()
    root = get_root_dir() / "Libs"
    for lib in root.iterdir():
        if not (lib / "conanfile.py ").exists():
            continue
        for config in ["Release", "Debug"]:
            if build_config(lib, config) != 0:
                print(F"ERROR in BUILD of {lib} config {config}", sys.stderr)
                exit(-666)


if __name__ == "__main__":
    main()
