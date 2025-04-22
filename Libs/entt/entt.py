"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class EnttHeader(Recipe):
    """
    Header-only version
    """

    name = "entt"
    version = "3.15.0"
    source_dir = "entt"
    kind = "header"

    def configure(self):
        self.cache_variables["ENTT_INSTALL"] = "ON"
