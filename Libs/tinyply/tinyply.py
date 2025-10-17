"""
Depmanager recipes
"""

from pathlib import Path

from depmanager.api.recipe import Recipe

here = Path(__file__).parent

cmakelists_modif = [
    "CMakeLists.txt",
]
corrections = [
    [
        b"cmake_minimum_required(VERSION 2.8.12)",
        b"cmake_minimum_required(VERSION 3.5)",
        None,
    ],
]


class TinyPlyShared(Recipe):
    """
    Shared version
    """

    name = "tinyply"
    version = "2.3.4"
    source_dir = "tinyply"
    kind = "shared"

    def source(self):
        for cmakelists in cmakelists_modif:
            path = self.path / self.source_dir / cmakelists
            if not path.exists():
                print(f"Error: file {cmakelists} @ {path} not found...")
                continue
            with open(path, "rb") as fp:
                lines = fp.read()
            for correction in corrections:
                if correction[2] not in [None, ""]:
                    if correction[2] != cmakelists:
                        continue
                lines = lines.replace(correction[0], correction[1])
            with open(path, "wb") as fp:
                fp.write(lines)
            print(f"***** File {cmakelists} @ {path} found and modified.")

    def clean(self):
        for cmakelists in cmakelists_modif:
            path = self.path / self.source_dir / cmakelists
            if not path.exists():
                print(f"Error: file {cmakelists} @ {path} not found...")
                continue
            with open(path, "rb") as fp:
                lines = fp.read()
            for correction in corrections:
                if correction[2] not in [None, ""]:
                    if correction[2] != cmakelists:
                        continue
                lines = lines.replace(correction[1], correction[0])
                pass
            with open(path, "wb") as fp:
                fp.write(lines)
            print(f"***** File {cmakelists} @ {path} restored.")

    def configure(self):
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"


class TinyPlyStatic(TinyPlyShared):
    """
    Static  version
    """

    kind = "static"
