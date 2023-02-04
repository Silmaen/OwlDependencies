from functions import *


def get_lib_dir():
    return get_root_dir() / "Libs"


class Library:
    path = Path()
    config = []
    depends = []

    def __init__(self, name: str):
        self.path = get_lib_dir() / name
        if not self.__is_valid():
            self.__void()
            return
        self.analyse()

    def __is_valid(self):
        if self.path == Path():
            return False
        return self.path.exists()

    def __void(self):
        self.path = Path()
        self.config = []
        self.depends = []

    def __repr__(self) -> str:
        rep = self.path.name
        if self.is_header_only():
            rep += " [ header only ]"
        else:
            rep += " [" + ", ".join(self.config) + "]"
        if self.has_depends():
            rep += " <== (" + ", ".join(self.depends) + ")"
        return rep

    def is_header_only(self):
        return len(self.config) == 0

    def has_depends(self):
        return len(self.depends) > 0

    def analyse(self):
        if (self.path / "configs").exists():
            with open(self.path / "configs") as fc:
                self.config = [l.strip() for l in fc.readlines()]
        if (self.path / "depends").exists():
            with open(self.path / "depends") as fc:
                self.depends = [l.strip() for l in fc.readlines()]


def get_ordered_libs(name: str = ""):
    is_ok = name == ""
    raw_list = []
    for lib in get_lib_dir().iterdir():
        if not (lib / "conanfile.py").exists():
            continue
        raw_list.append(Library(lib.name))
        if not is_ok and lib.name == name:
            return [Library(lib.name)]
    if not is_ok:
        log(F"Library {name} not found", levels["error"])
        return []
    # ordering the list
    ordered_list = []
    ordered_list_name = []
    while len(raw_list) > 0:
        for lib in raw_list:
            if not lib.has_depends():
                ordered_list.append(lib)
                ordered_list_name.append(lib.path.name)
                raw_list.remove(lib)
                continue
            all_deps = True
            for dep in lib.depends:
                if dep not in ordered_list_name:
                    all_deps = False
                    break
            if all_deps:
                ordered_list.append(lib)
                ordered_list_name.append(lib.path.name)
                raw_list.remove(lib)
    return ordered_list
