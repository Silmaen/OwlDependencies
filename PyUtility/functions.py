from pathlib import Path


def get_root_dir():
    return Path(__file__).parent.parent


def mk_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def get_tmp_dir():
    tmp = get_root_dir() / "tmp"
    if not tmp.exists():
        mk_dir(tmp)
    return tmp


def clean_tmp():
    tmp = get_root_dir() / "tmp"
    if tmp.exists():
        tmp.rmdir()


def mk_build_dir():
    build = get_root_dir() / "build"
    if not build.exists():
        mk_dir(build)
    return build


def clean_build():
    tmp = get_root_dir() / "build"
    if tmp.exists():
        tmp.rmdir()


def run(cmd: str):
    import sys
    from subprocess import run
    try:
        ret = run(cmd, shell=True)
        if ret.returncode != 0:
            print(F"ERROR during run code {ret.returncode}", file=sys.stderr)
            return ret.returncode
    except Exception as err:
        print(F"EXCEPTION during run {err}", file=sys.stderr)
        return -666
    return 0

