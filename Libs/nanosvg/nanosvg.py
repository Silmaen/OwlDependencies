"""
Depmanager recipes
"""

from pathlib import Path

from depmanager.api.recipe import Recipe

here = Path(__file__).parent


class NanoSvgHeader(Recipe):
    """
    Header-only version
    """

    name = "nanosvg"
    version = "1.0.0"
    source_dir = "nanosvg"
    kind = "static"
