"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class ImguiNodeEditor(Recipe):
    """
    Static version
    """

    name = "imgui_node_editor"
    version = "0.9.3"
    source_dir = "sources"
    kind = "static"
    dependencies = [
        {"name": "imgui", "kind": "shared"},
        {"name": "vulkan_sdk", "kind": "shared"},
    ]
    description = "Node editor built around Dear ImGui."

    def configure(self):
        self.cache_variables["PROJECT_VERSION"] = self.version
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"
