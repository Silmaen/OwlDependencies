"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class ImguizmoShared(Recipe):
    """
    Shared version
    """
    name = "imguizmo"
    version = "1.90.0"
    source_dir = "sources"
    kind = "shared"
    dependencies = [{"name": "imgui", "kind": "shared"}]


class ImguizmoStatic(Recipe):
    """
    Shared version
    """
    name = "imguizmo"
    version = "1.90.0"
    source_dir = "sources"
    kind = "static"
    dependencies = [{"name": "imgui", "kind": "static"}]
