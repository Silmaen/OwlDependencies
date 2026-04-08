"""
Depmanager recipes
"""

from pathlib import Path

from depmanager.api.recipe import Recipe

here = Path(__file__).parent


class NanoSvg(Recipe):
    """
    Header version
    """

    name = "nanosvg"
    version = "1.0.0"
    source_dir = "nanosvg"
    kind = "header"
    description = "NanoSVG is a simple SVG parser and rasterizer"
