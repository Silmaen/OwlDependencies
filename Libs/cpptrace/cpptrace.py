"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class CppTraceShared(Recipe):
    """
    Shared version
    """
    name = "cpptrace"
    version = "0.1"
    source_dir = "cpptrace"
    kind = "shared"


class CppTraceStatic(Recipe):
    """
    Shared version
    """
    name = "cpptrace"
    version = "0.1"
    source_dir = "cpptrace"
    kind = "static"
