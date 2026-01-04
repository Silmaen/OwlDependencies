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
    version = "1.0.3"
    source_dir = "sources/glm"
    kind = "shared"
    description = "GLM is a header only C++ mathematics library for graphics software based on the OpenGL Shading Language (GLSL) specifications."

    def configure(self):
        self.cache_variables["GLM_ENABLE_CXX_20"] = "ON"
        self.cache_variables["GLM_BUILD_TESTS"] = "OFF"
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"


class GlmStatic(GlmShared):
    """
    Static version
    """

    kind = "static"
