import argparse
import os
import platform
import re
import subprocess
from pathlib import Path


def get_edm_basedir():
    try:
        result = subprocess.run(
            ["dmgr", "info", "basedir"], capture_output=True, text=True, check=True
        )
        return Path(result.stdout.strip())
    except subprocess.CalledProcessError:
        print("Erreur : Impossible de déterminer le chemin de base de .edm.")
        return None


def is_ignored(lib_name, ignore_list):
    return any(ignore in lib_name for ignore in ignore_list)


def is_in_lib_dir(lib_path, lib_dir):
    return str(lib_path).startswith(str(lib_dir))


def check_shared_lib_linux(lib, lib_dir, ignore_list):
    try:
        result = subprocess.run(
            ["ldd", str(lib)], capture_output=True, text=True, check=True
        )
        non_system_deps = []

        for line in result.stdout.splitlines():
            if "=>" not in line:
                continue
            parts = line.split("=>", 1)

            lib_name = parts[0].strip()
            lib_path = parts[1].strip().split()[0]

            if not is_ignored(lib_name, ignore_list) and not is_in_lib_dir(
                lib_path, lib_dir
            ):
                non_system_deps.append(lib_name)

        if non_system_deps:
            print(lib)
            for dep in non_system_deps:
                print(f"    {dep}")
    except subprocess.CalledProcessError:
        pass


def check_dll_dependencies_windows(dll, lib_dir, ignore_list):
    try:
        result = subprocess.run(
            ["objdump", "-p", str(dll)], capture_output=True, text=True, check=True
        )
        non_system_deps = []

        for line in result.stdout.splitlines():
            if "DLL Name" in line:
                dep = line.split()[-1]
                dep_path = lib_dir / dep

                if not is_ignored(dep, ignore_list) and not is_in_lib_dir(
                    dep_path, lib_dir
                ):
                    non_system_deps.append(dep)

        if non_system_deps:
            print(dll)
            for dep in non_system_deps:
                print(f"    {dep}")
    except subprocess.CalledProcessError:
        pass


def main():
    parser = argparse.ArgumentParser(description="Check library dependencies.")
    parser.add_argument(
        "filter", nargs="?", default=".*", help="Regex filter for library names."
    )
    args = parser.parse_args()

    edm_basedir = get_edm_basedir()
    if not edm_basedir:
        return

    lib_dir = edm_basedir / "data"
    ignore_list = [
        "libc",
        "libgcc",
        "libm",
        "libstdc++",
        "ld-linux-x86-64",
        "linux-vdso",
        "libatomic",
        "libGL",
        "libX11",
        "libGLX",
        "libxcb",
        "libXau",
        "libXdmcp",
        "libbsd",
        "libssl",
        "libcrypto",
        "kernel32.dll",
        "user32.dll",
        "gdi32.dll",
        "winspool.drv",
        "comdlg32.dll",
        "advapi32.dll",
        "shell32.dll",
        "ole32.dll",
        "oleaut32.dll",
        "uuid.dll",
        "odbc32.dll",
        "odbccp32.dll",
    ]

    filter_regex = re.compile(args.filter)

    if platform.system() == "Linux":
        # add
        lib_subdirs = list(set([str(p.parent) for p in lib_dir.rglob("*.so*")]))
        os.environ["LD_LIBRARY_PATH"] = (
            ":".join(lib_subdirs) + ":" + os.environ.get("LD_LIBRARY_PATH", "")
        )

        for lib in lib_dir.rglob("*.so"):
            if filter_regex.match(lib.name):
                check_shared_lib_linux(lib, lib_dir, ignore_list)

    elif platform.system() == "Windows":
        for dll in lib_dir.rglob("*.dll"):
            if filter_regex.match(dll.name):
                check_dll_dependencies_windows(dll, lib_dir, ignore_list)

    else:
        print("Système d'exploitation non supporté.")


if __name__ == "__main__":
    main()
