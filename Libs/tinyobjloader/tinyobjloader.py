"""
Depmanager recipes
"""

from pathlib import Path

from depmanager.api.recipe import Recipe

here = Path(__file__).parent


class TinyObjLoaderShared(Recipe):
    """
    Shared version
    """

    name = "tinyobjloader"
    version = "2.0.0-rc13"
    source_dir = "tinyobjloader"
    kind = "shared"

    def configure(self):
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"


class TinyObjLoaderStatic(TinyObjLoaderShared):
    """
    Static  version
    """

    kind = "static"
