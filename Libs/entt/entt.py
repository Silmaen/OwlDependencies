"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class EnttHeader(Recipe):
    """
    Header-only version
    """

    name = "entt"
    version = "3.16.0"
    source_dir = "entt"
    kind = "header"
    description = "EnTT is a fast and reliable entity-component-system (ECS) and much more for C++"

    def configure(self):
        self.cache_variables["ENTT_INSTALL"] = "ON"
