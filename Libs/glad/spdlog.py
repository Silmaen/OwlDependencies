"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class GladShared(Recipe):
    """
    Shared version
    """
    name = "glad"
    version = "0.1.36"
    source_dir = "sources"
    kind = "shared"


class GladStatic(Recipe):
    """
    Shared version
    """
    name = "glad"
    version = "0.1.36"
    source_dir = "sources"
    kind = "static"

