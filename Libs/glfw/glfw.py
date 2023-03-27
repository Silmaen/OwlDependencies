"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class GlfwShared(Recipe):
    """
    Shared version
    """
    name = "glfw"
    version = "3.3.8"
    source_dir = "glfw"
    kind = "shared"

    def configure(self):
        self.cache_variables["GLFW_BUILD_EXAMPLES"] = "OFF"
        self.cache_variables["GLFW_BUILD_TESTS"] = "OFF"
        self.cache_variables["GLFW_BUILD_DOCS"] = "OFF"


class GlfwStatic(Recipe):
    """
    Shared version
    """
    name = "glfw"
    version = "3.3.8"
    source_dir = "glfw"
    kind = "static"

    def configure(self):
        self.cache_variables["GLFW_BUILD_EXAMPLES"] = "OFF"
        self.cache_variables["GLFW_BUILD_TESTS"] = "OFF"
        self.cache_variables["GLFW_BUILD_DOCS"] = "OFF"

