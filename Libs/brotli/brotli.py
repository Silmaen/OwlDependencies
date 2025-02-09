"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class BrotliShared(Recipe):
    """
    Shared version
    """

    name = "brotli"
    version = "1.1.0"
    source_dir = "brotli"
    kind = "shared"

    def configure(self):
        self.cache_variables["BROTLI_DISABLE_TESTS"] = "ON"


class BrotliStatic(BrotliShared):
    """
    Static version
    """

    kind = "static"
