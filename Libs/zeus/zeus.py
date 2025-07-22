"""
Depmanager recipes
"""

from pathlib import Path

from depmanager.api.recipe import Recipe

here = Path(__file__).parent


class ZeusHeader(Recipe):
    """
    Header-only version
    """

    name = "zeus"
    version = "1.3.1"
    source_dir = "expected"
    kind = "header"

    def configure(self):
        self.cache_variables["BUILD_TESTING"] = "OFF"
