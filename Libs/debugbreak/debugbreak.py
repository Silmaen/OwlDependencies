"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class DebugBreakHeader(Recipe):
    """
    Header-only version
    """
    name = "debugbreak"
    version = "1.0"
    source_dir = "sources"
    kind = "header"
