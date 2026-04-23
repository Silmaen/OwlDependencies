"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class ImguiMarkdown(Recipe):
    """
    Header-only version
    """

    name = "imgui_markdown"
    version = "1.92.7"
    source_dir = "sources"
    kind = "header"
    dependencies = [
        {"name": "imgui", "kind": "shared"},
        {"name": "vulkan_sdk", "kind": "shared"},
    ]
    description = "Markdown rendering for Dear ImGui using the same API."

    def configure(self):
        self.cache_variables["PROJECT_VERSION"] = self.version
