"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe

file_modif = [
    "CMakeLists.txt",
]
corrections = [
    [
        b"cmake_minimum_required (VERSION 3.1..3.18)",
        b"cmake_minimum_required (VERSION 3.5)",
        None,
    ],
]


class LibSndFileShared(Recipe):
    """
    Shared version
    """

    name = "libsndfile"
    version = "1.2.2"
    source_dir = "libsndfile"
    kind = "shared"

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
        self.cache_variables["BUILD_TESTING"] = "OFF"
        self.cache_variables["INSTALL_PKGCONFIG_MODULE"] = "OFF"
        self.cache_variables["BUILD_EXAMPLES"] = "OFF"
        self.cache_variables["BUILD_PROGRAMS"] = "OFF"
        self.cache_variables["BUILD_REGTEST"] = "OFF"
        self.cache_variables["INSTALL_MANPAGES"] = "OFF"
        self.cache_variables["ENABLE_MPEG"] = "OFF"
        self.cache_variables["ENABLE_EXTERNAL_LIBS"] = "OFF"
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"


class LibSndFileStatic(LibSndFileShared):
    """
    Static version
    """

    kind = "static"
