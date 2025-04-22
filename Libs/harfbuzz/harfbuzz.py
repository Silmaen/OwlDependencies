"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class HarfbuzzStatic(Recipe):
    """
    Shared version
    """

    name = "harfbuzz"
    version = "11.1.0"
    source_dir = "harfbuzz"
    kind = "static"

    def configure(self):
        self.cache_variables["HB_BUILD_UTILS"] = "OFF"
