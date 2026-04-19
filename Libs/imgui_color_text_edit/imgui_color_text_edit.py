"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class ImguiColorTextEdit(Recipe):
    """
    Static version
    """

    name = "imgui_color_text_edit"
    version = "1.92.7"
    source_dir = "sources"
    kind = "static"
    dependencies = [
        {"name": "imgui", "kind": "shared"},
        {"name": "vulkan_sdk", "kind": "shared"},
    ]
    description = "Syntax highlighting text editor for Dear ImGui."

    def configure(self):
        self.cache_variables["PROJECT_VERSION"] = self.version
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"
