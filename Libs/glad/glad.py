"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class GladSharedNew(Recipe):
    """
    Shared version
    """
    name = "glad"
    version = "2.0.4"
    source_dir = "sources"
    kind = "shared"


class GladStaticNew(Recipe):
    """
    Shared version
    """
    name = "glad"
    version = "2.0.4"
    source_dir = "sources"
    kind = "static"
