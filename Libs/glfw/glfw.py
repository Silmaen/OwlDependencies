"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class GlfwShared(Recipe):
    """
    Shared version
    """

    name = "glfw"
    version = "3.3.9"
    source_dir = "glfw"
    kind = "shared"

    def configure(self):
        self.cache_variables["GLFW_BUILD_EXAMPLES"] = "OFF"
        self.cache_variables["GLFW_BUILD_TESTS"] = "OFF"
        self.cache_variables["GLFW_BUILD_DOCS"] = "OFF"
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"


class GlfwStatic(GlfwShared):
    """
    Static version
    """

    kind = "static"
