"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class GladShared(Recipe):
    """
    Shared version
    """

    name = "glad"
    version = "2.0.4"
    source_dir = "sources"
    kind = "shared"


class GladStatic(GladShared):
    """
    Static version
    """

    kind = "static"
