"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class ImguizmoShared(Recipe):
    """
    Shared version
    """

    name = "imguizmo"
    version = "1.91.9b"
    source_dir = "sources"
    kind = "shared"
    dependencies = [
        {"name": "imgui", "kind": "shared"},
        {"name": "vulkan_sdk", "kind": "shared"},
    ]

    def configure(self):
        self.cache_variables["PROJECT_VERSION"] = self.version
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"


class ImguizmoStatic(ImguizmoShared):
    """
    Shared version
    """

    kind = "static"
    dependencies = [
        {"name": "imgui", "kind": "static"},
        {"name": "vulkan_sdk", "kind": "shared"},
    ]
