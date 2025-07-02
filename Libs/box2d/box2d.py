"""
Depmanager recipes
"""

from pathlib import Path
from shutil import copy2

from depmanager.api.recipe import Recipe

here = Path(__file__).resolve().parent
modifications = here / "modifs"

cmakelists_modif = [
    "src/CMakeLists.txt",
]
corrections = [
    [
        b"install(TARGETS box2d)",
        b"SET(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR})\ninclude(DmgrInstall)",
        None,
    ],
    [
        b"$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>",
        b"$<INSTALL_INTERFACE:include>",
        None,
    ],
]


class Box2DShared(Recipe):
    """
    Shared version
    """

    name = "box2d"
    version = "3.1.1"
    source_dir = "box2d"
    kind = "shared"
    dependencies = []

    def source(self):
        source = here / self.source_dir
        copy2(modifications / "box2d-config.cmake.in", source / "box2d-config.cmake.in")
        copy2(modifications / "DmgrInstall.cmake", source / "DmgrInstall.cmake")
        # Files to modify
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
        source = here / self.source_dir
        (source / "box2d-config.cmake.in").unlink()
        (source / "DmgrInstall.cmake").unlink()
        # Files to restore
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
        self.cache_variables["BUILD_SHARED_LIBS"] = "ON"
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"
        self.cache_variables["BOX2D_SAMPLES"] = "OFF"
        self.cache_variables["BOX2D_VALIDATE"] = "OFF"
        self.cache_variables["BOX2D_UNIT_TESTS"] = "OFF"


class Box2DStatic(Box2DShared):
    """
    Static version
    """

    kind = "static"
    dependencies = []

    def configure(self):
        self.cache_variables["BUILD_SHARED_LIBS"] = "OFF"
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"
        self.cache_variables["BOX2D_SAMPLES"] = "OFF"
        self.cache_variables["BOX2D_VALIDATE"] = "OFF"
        self.cache_variables["BOX2D_UNIT_TESTS"] = "OFF"
