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
        {"name": "vulkan", "kind": "shared"},
    ]


class ImguiStatic(ImguiShared):
    """
    Static version
    """

    kind = "static"
    dependencies = [
        {"name": "glfw", "kind": "static"},
        {"name": "vulkan", "kind": "static"},
    ]
