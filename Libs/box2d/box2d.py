"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class Box2DShared(Recipe):
    """
    Shared version
    """

    name = "box2d"
    version = "3.0.0"
    source_dir = "box2d"
    kind = "shared"
    dependencies = []

    def configure(self):
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"
        self.cache_variables["BOX2D_SAMPLES"] = "OFF"
        self.cache_variables["BOX2D_VALIDATE"] = "OFF"
        self.cache_variables["BOX2D_UNIT_TESTS"] = "OFF"


class Box2DStatic(Box2DShared):
    """
    Static version
    """

    kind = "static"
    dependencies = []
