"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe

cmakelists_modif = [
    "CMakeLists.txt",
    "src/lib/libdwarf/CMakeLists.txt",
    "src/lib/libdwarf/cmake/libdwarfConfig.cmake.in",
]
corrections = [
    [b"find_package(zstd)", b"find_package(zstd CONFIG)", None],
    [b"find_package(ZLIB)", b"find_package(ZLIB CONFIG)", None],
    [
        b'install(FILES "${PROJECT_SOURCE_DIR}/cmake/Findzstd.cmake")',
        b'#install(FILES "${' b'PROJECT_SOURCE_DIR}/cmake/Findzstd.cmake")',
        None,
    ],
    [b"find_dependency(zstd)", b"find_dependency(zstd CONFIG)", None],
    [b"find_dependency(ZLIB)", b"find_dependency(ZLIB CONFIG)", None],
]


class LibDwarfShared(Recipe):
    """
    Shared version
    """

    name = "libdwarf"
    version = "0.12.0"
    source_dir = "libdwarf-code"
    kind = "shared"
    dependencies = [
        {"name": "zstd", "kind": "static"},
        {"name": "zlib", "kind": "static"},
    ]

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
        self.cache_variables["BUILD_DWARFDUMP"] = "OFF"
        self.cache_variables["BUILD_SHARED"] = "ON"
        self.cache_variables["BUILD_NON_SHARED"] = "OFF"


class CppTraceStatic(LibDwarfShared):
    """
    Static version
    """

    kind = "static"
    dependencies = [
        {"name": "zstd", "kind": "static"},
        {"name": "zlib", "kind": "static"},
    ]

    def configure(self):
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"
        self.cache_variables["BUILD_DWARFDUMP"] = "OFF"
        self.cache_variables["BUILD_SHARED"] = "OFF"
        self.cache_variables["BUILD_NON_SHARED"] = "ON"
