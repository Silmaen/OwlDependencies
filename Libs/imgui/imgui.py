"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class ImguiShared(Recipe):
    """
    Shared version
    """

    name = "imgui"
    version = "1.90.1-docking"
    source_dir = "sources"
    kind = "shared"
    dependencies = [
        {"name": "glfw", "kind": "shared"},
        {"name": "vulkan_sdk", "kind": "shared"},
    ]

    def configure(self):
        self.cache_variables["PROJECT_VERSION"] = self.version.split("-")[0]


class ImguiStatic(ImguiShared):
    """
    Static version
    """

    kind = "static"
    dependencies = [
        {"name": "glfw", "kind": "static"},
        {"name": "vulkan_sdk", "kind": "shared"},
    ]
