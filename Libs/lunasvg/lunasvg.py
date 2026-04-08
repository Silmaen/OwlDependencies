"""
Depmanager recipes
"""

from pathlib import Path

from depmanager.api.recipe import Recipe

here = Path(__file__).parent


class LunaSvgStatic(Recipe):
    """
    StaticLib version
    """

    name = "lunasvg"
    version = "3.5.0"
    source_dir = "lunasvg"
    kind = "static"
    description = "LunaSVG is a C++ library for parsing and rasterizing SVG files. It is designed to be fast and easy to use, and it supports a wide range of SVG features."

    def configure(self):
        self.cache_variables["LUNASVG_BUILD_EXAMPLES"] = False
        self.cache_variables["PLUTOVG_BUILD_EXAMPLES"] = False


class LunaSvgShared(LunaSvgStatic):
    """
    SharedLib version
    """

    kind = "shared"
