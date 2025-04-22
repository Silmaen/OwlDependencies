"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe

file_modif = [
    "CMakeLists.txt",
    "scripts/cmake/PNGConfig.cmake",
]
corrections = [
    [b"find_package(ZLIB", b"find_package(ZLIB CONFIG", None],
    [b"find_dependency(ZLIB", b"find_dependency(ZLIB CONFIG", None],
]


class LibPngShared(Recipe):
    """
    Shared version
    """

    name = "libpng"
    version = "1.6.47"
    source_dir = "libpng"
    kind = "shared"
    dependencies = [{"name": "zlib", "kind": "static"}]

    def source(self):
        # Files to modify
        for file in file_modif:
            path = self.path / self.source_dir / file
            if not path.exists():
                print(f"Error: file {file} @ {path} not found...")
                continue
            with open(path, "rb") as fp:
                lines = fp.read()
            for correction in corrections:
                if correction[2] not in [None, ""]:
                    if correction[2] != file:
                        continue
                lines = lines.replace(correction[0], correction[1])
            with open(path, "wb") as fp:
                fp.write(lines)
            print(f"***** File {file} @ {path} found and modified.")

    def clean(self):
        # Files to restore
        for file in file_modif:
            path = self.path / self.source_dir / file
            if not path.exists():
                print(f"Error: file {file} @ {path} not found...")
                continue
            with open(path, "rb") as fp:
                lines = fp.read()
            for correction in corrections:
                if correction[2] not in [None, ""]:
                    if correction[2] != file:
                        continue
                lines = lines.replace(correction[1], correction[0])
                pass
            with open(path, "wb") as fp:
                fp.write(lines)
            print(f"***** File {file} @ {path} restored.")

    def configure(self):
        self.cache_variables["PNG_SHARED"] = "ON"
        self.cache_variables["PNG_STATIC"] = "OFF"
        self.cache_variables["PNG_TESTS"] = "OFF"
        self.cache_variables["PNG_TOOLS"] = "OFF"
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"
        self.cache_variables["AWK"] = "OFF"


class LibPngStatic(LibPngShared):
    """
    Static version
    """

    kind = "static"
    dependencies = [{"name": "zlib", "kind": "static"}]

    def configure(self):
        super().configure()
        self.cache_variables["PNG_SHARED"] = "OFF"
        self.cache_variables["PNG_STATIC"] = "ON"
