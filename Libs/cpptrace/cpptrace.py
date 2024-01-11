"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class CppTraceShared(Recipe):
    """
    Shared version
    """
    name = "cpptrace"
    version = "0.3.1"
    source_dir = "cpptrace"
    kind = "shared"
    config = ["Release"]


class CppTraceStatic(CppTraceShared):
    """
    Shared version
    """
    kind = "static"
