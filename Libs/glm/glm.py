"""
Depmanager recipes
"""
from pathlib import Path

from depmanager.api.recipe import Recipe

here = Path(__file__).parent


class GlmShared(Recipe):
    """
    Shared version
    """

    name = "glm"
    version = "0.9.9.9"
    source_dir = "sources/glm"
    kind = "shared"

    def configure(self):
        self.cache_variables["GLM_BUILD_TESTS"] = "OFF"
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"


class GlmStatic(GlmShared):
    """
    Static version
    """

    kind = "static"
