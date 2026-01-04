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
    version = "2.9.7"
    source_dir = "tinygltf"
    kind = "header"
    description = "TinyGLTF is a header only C++11 glTF 2.0 library"

    def configure(self):
        self.cache_variables["TINYGLTF_BUILD_LOADER_EXAMPLE"] = "OFF"
        self.cache_variables["TINYGLTF_HEADER_ONLY"] = "ON"
        self.cache_variables["TINYGLTF_INSTALL_VENDOR"] = "ON"
