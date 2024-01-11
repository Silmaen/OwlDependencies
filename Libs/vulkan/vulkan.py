"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe

ignore_list = ["BUILD_TESTING"]


class VulkanShared(Recipe):
    """
    Shared version
    """

    name = "vulkan"
    version = "1.3.275"
    source_dir = "source"
    kind = "shared"

    def configure(self):
        self.cache_variables["VK_VERSION_STRING"] = f"{self.version}"
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"


class VulkanStatic(VulkanShared):
    """
    Static version
    """

    kind = "static"
