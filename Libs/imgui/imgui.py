"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class ImguiShared(Recipe):
    """
    Shared version
    """
    name = "imgui"
    version = "1.90.0-docking"
    source_dir = "sources"
    kind = "shared"
    dependencies = [{"name": "glfw", "kind": "shared"}]


class ImguiStatic(Recipe):
    """
    Shared version
    """
    name = "imgui"
    version = "1.90.0-docking"
    source_dir = "sources"
    kind = "static"
    dependencies = [{"name": "glfw", "kind": "static"}]
