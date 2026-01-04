"""
Depmanager recipes
"""

from pathlib import Path

from depmanager.api.recipe import Recipe

here = Path(__file__).parent

file_modif = [
    "common/altypes.hpp",
]
corrections = [
    [
        b"#include <cstdio>\n#include <cstddef>",
        b"#include <cstdio>\n#include <cstddef>\n#include <cstdint>",
        None,
    ],
]


class OpenALShared(Recipe):
    """
    Shared version (the only one)
    """

    name = "openal"
    version = "1.25.0"
    source_dir = "openal-soft"
    kind = "shared"
    description = "Cross-platform 3D audio API appropriate for gaming applications"

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
        self.cache_variables["ALSOFT_EXAMPLES"] = "OFF"
        self.cache_variables["ALSOFT_INSTALL_EXAMPLES"] = "OFF"
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"
