"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class Implot(Recipe):
    """
    Static version
    """

    name = "implot"
    version = "1.0"
    source_dir = "sources"
    kind = "static"
    dependencies = [
        {"name": "imgui", "kind": "shared"},
        {"name": "vulkan_sdk", "kind": "shared"},
    ]
    description = "Advanced 2D Plotting for Dear ImGui."

    def configure(self):
        self.cache_variables["PROJECT_VERSION"] = self.version
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"
