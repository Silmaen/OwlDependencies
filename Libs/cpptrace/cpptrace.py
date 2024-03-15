"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class CppTraceShared(Recipe):
    """
    Shared version
    """

    name = "cpptrace"
    version = "0.4.1"
    source_dir = "cpptrace"
    kind = "shared"

    def configure(self):
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"


class CppTraceStatic(CppTraceShared):
    """
    Shared version
    """

    kind = "static"
