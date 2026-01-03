"""
Depmanager recipes
"""

from pathlib import Path
from shutil import copy2

from depmanager.api.recipe import Recipe

here = Path(__file__).resolve().parent
modifications = here / "modifs"

corrections = [
    [
        b"# Example binaries",
        b"SET(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR})\ninclude(DmgrInstall)",
    ],
    [
        b"target_include_directories(zlib PUBLIC ${CMAKE_CURRENT_BINARY_DIR} ${CMAKE_CURRENT_SOURCE_DIR})",
        b"target_include_directories(zlib PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}> $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}> $<INSTALL_INTERFACE:include>)",
    ],
    [
        b"target_include_directories(zlibstatic PUBLIC ${CMAKE_CURRENT_BINARY_DIR} ${CMAKE_CURRENT_SOURCE_DIR})",
        b"target_include_directories(zlibstatic PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}> $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}> $<INSTALL_INTERFACE:include>)",
    ],
]


class ZlibShared(Recipe):
    """
    Shared version
    """

    name = "zlib"
    version = "1.3.1.2"
    source_dir = "zlib"
    kind = "shared"

    def source(self):
        source = here / self.source_dir
        copy2(modifications / "zlib-config.cmake.in", source / "zlib-config.cmake.in")
        copy2(modifications / "DmgrInstall.cmake", source / "DmgrInstall.cmake")
        # modify CMakeLists.txt
        with open(source / "CMakeLists.txt", "rb") as fp:
            lines = fp.read()
            for correction in corrections:
                lines = lines.replace(correction[0], correction[1])
            lines = lines.replace(b"# Example binaries", b"include(DmgrInstall)")
        with open(source / "CMakeLists.txt", "wb") as fp:
            fp.write(lines)

    def configure(self):
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"
        self.cache_variables["ZLIB_BUILD_EXAMPLES"] = "OFF"
        self.cache_variables["SKIP_INSTALL_FILES"] = "ON"

    def clean(self):
        source = here / self.source_dir
        (source / "zlib-config.cmake.in").unlink()
        (source / "DmgrInstall.cmake").unlink()
        # restore CMakeLists.txt
        with open(source / "CMakeLists.txt", "rb") as fp:
            lines = fp.read()
            for correction in corrections:
                lines = lines.replace(correction[1], correction[0])
        with open(source / "CMakeLists.txt", "wb") as fp:
            fp.write(lines)


class ZlibStatic(ZlibShared):
    """
    Static version
    """

    kind = "static"

    def configure(self):
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"
        self.cache_variables["ZLIB_BUILD_EXAMPLES"] = "OFF"
        self.cache_variables["SKIP_INSTALL_FILES"] = "ON"
