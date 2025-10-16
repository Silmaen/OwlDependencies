"""
Depmanager recipes
"""

from pathlib import Path

from depmanager.api.recipe import Recipe

here = Path(__file__).parent


class TinyPlyShared(Recipe):
    """
    Shared version
    """

    name = "tinyply"
    version = "2.3.4"
    source_dir = "tinyply"
    kind = "shared"

    def configure(self):
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"


class TinyPlyStatic(TinyPlyShared):
    """
    Static  version
    """

    kind = "static"
