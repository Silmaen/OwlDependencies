"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class GlmShared(Recipe):
    """
    Shared version
    """
    name = "glm"
    version = "0.9.9.8"
    source_dir = "sources"
    kind = "shared"

    def configure(self):
        self.cache_variables["BUILD_STATIC_LIBS"] = "OFF"


class GlmStatic(Recipe):
    """
    Shared version
    """
    name = "glm"
    version = "0.9.9.8"
    source_dir = "sources"
    kind = "static"

    def configure(self):
        self.cache_variables["BUILD_STATIC_LIBS"] = "ON"

