"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class ImguiShared(Recipe):
    """
    Shared version
    """

    name = "imgui"
    version = "1.91.5-docking"
    source_dir = "sources"
    kind = "shared"
    dependencies = [
        {"name": "glfw", "kind": "shared"},
        {"name": "vulkan_sdk", "kind": "shared"},
    ]

    def configure(self):
        self.cache_variables["PROJECT_VERSION"] = self.version.split("-")[0]
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"


class ImguiStatic(ImguiShared):
    """
    Static version
    """

    kind = "static"
    dependencies = [
        {"name": "glfw", "kind": "static"},
        {"name": "vulkan_sdk", "kind": "shared"},
    ]
