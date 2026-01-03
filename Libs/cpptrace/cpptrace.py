"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe

cmakelists_modif = [
    "src/binary/object.cpp",
]
corrections = [
    [
        b"#define WIN32_LEAN_AND_MEAN",
        b"#define WIN32_LEAN_AND_MEAN\n#include <system_error>",
        None,
    ],
]


class CppTraceShared(Recipe):
    """
    Shared version
    """

    name = "cpptrace"
    version = "1.0.4"
    source_dir = "cpptrace"
    kind = "shared"
    dependencies = [
        {"name": "zstd", "kind": "static"},
        {"name": "libdwarf", "kind": "static"},
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
        self.cache_variables["CPPTRACE_USE_EXTERNAL_LIBDWARF"] = "ON"
        self.cache_variables["CPPTRACE_USE_EXTERNAL_ZSTD"] = "ON"
        self.cache_variables["CPPTRACE_VCPKG"] = "ON"
        self.cache_variables["CPPTRACE_POSITION_INDEPENDENT_CODE"] = "ON"


class CppTraceStatic(CppTraceShared):
    """
    Static version
    """

    kind = "static"
    dependencies = [
        {"name": "zstd", "kind": "static"},
        {"name": "libdwarf", "kind": "static"},
    ]
