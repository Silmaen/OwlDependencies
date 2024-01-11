"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class EnttHeader(Recipe):
    """
    Header-only version
    """
    name = "entt"
    version = "3.12.2"
    source_dir = "entt"
    kind = "header"
