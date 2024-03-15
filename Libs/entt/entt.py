"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class EnttHeader(Recipe):
    """
    Header-only version
    """
    name = "entt"
    version = "3.13.1"
    source_dir = "entt"
    kind = "header"
