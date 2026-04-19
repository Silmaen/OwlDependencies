"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class Imguizmo(Recipe):
    """
    Static version
    """

    name = "imguizmo"
    version = "1.92.7"
    source_dir = "sources"
    kind = "static"
    dependencies = [
        {"name": "imgui", "kind": "shared"},
        {"name": "vulkan_sdk", "kind": "shared"},
    ]
    description = "ImGuizmo is a simple and easy to use gizmo for manipulating objects in 3D space with Dear ImGui."

    def configure(self):
        self.cache_variables["PROJECT_VERSION"] = self.version
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"
