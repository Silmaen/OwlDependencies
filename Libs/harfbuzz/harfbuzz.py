"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class HarfbuzzShared(Recipe):
    """
    Shared version
    """

    name = "harfbuzz"
    version = "10.2.0"
    source_dir = "harfbuzz"
    kind = "shared"

    def configure(self):
        self.cache_variables["HB_BUILD_UTILS"] = "OFF"


class HarfbuzzStatic(HarfbuzzShared):
    """
    Static version
    """

    kind = "static"
