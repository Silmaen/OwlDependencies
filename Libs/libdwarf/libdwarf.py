"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class CppTraceShared(Recipe):
    """
    Shared version
    """

    name = "libdwarf"
    version = "0.5.2"
    source_dir = "libdwarf-code"
    kind = "shared"

    def configure(self):
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"


class CppTraceStatic(CppTraceShared):
    """
    Shared version
    """

    kind = "static"
