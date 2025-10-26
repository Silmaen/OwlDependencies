"""
Depmanager recipes
"""

from pathlib import Path

from depmanager.api.recipe import Recipe

here = Path(__file__).parent


class TinyGltf(Recipe):
    """
    Shared version
    """

    name = "tinygltf"
    version = "2.9.6"
    source_dir = "tinygltf"
    kind = "header"

    def configure(self):
        self.cache_variables["TINYGLTF_BUILD_LOADER_EXAMPLE"] = "OFF"
        self.cache_variables["TINYGLTF_HEADER_ONLY"] = "ON"
        self.cache_variables["TINYGLTF_INSTALL_VENDOR"] = "ON"
