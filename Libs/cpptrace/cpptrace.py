"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class CppTraceShared(Recipe):
    """
    Shared version
    """

    name = "cpptrace"
    version = "0.7.2"
    source_dir = "cpptrace"
    kind = "shared"
    dependencies = [
        {"name": "zstd", "kind": "static"},
        {"name": "libdwarf", "kind": "static"},
        {"name": "zlib", "kind": "static"},
    ]

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
        {"name": "zlib", "kind": "static"},
    ]
