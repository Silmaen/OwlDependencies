"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe

file_modif = [
    "CMake/Macros.cmake",
    "CMake/curl-config.cmake.in",
]
corrections = [
    [b"find_package(${_dependency}", b"find_package(${_dependency} CONFIG", None],
    [b"find_dependency(ZLIB", b"find_dependency(ZLIB CONFIG", None],
]


class CurlShared(Recipe):
    """
    Shared version
    """

    name = "curl"
    version = "8.12.0"
    source_dir = "curl"
    kind = "shared"
    dependencies = [
        {"name": "zlib", "kind": "shared"},
        {"name": "zstd", "kind": "shared"},
        {"name": "brotli", "kind": "shared"},
    ]

    def configure(self):
        self.cache_variables["BUILD_CURL_EXE"] = "OFF"
        self.cache_variables["CURL_USE_LIBPSL"] = "OFF"
        self.cache_variables["BUILD_STATIC_LIBS"] = "OFF"
        self.cache_variables["BUILD_SHARED_LIBS"] = "ON"

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


class CurlStatic(CurlShared):
    """
    Static version
    """

    kind = "static"
    dependencies = [
        {"name": "zlib", "kind": "static"},
        {"name": "zstd", "kind": "static"},
        {"name": "brotli", "kind": "shared"},
    ]

    def configure(self):
        super().configure()
        self.cache_variables["BUILD_STATIC_LIBS"] = "ON"
        self.cache_variables["BUILD_SHARED_LIBS"] = "OFF"
