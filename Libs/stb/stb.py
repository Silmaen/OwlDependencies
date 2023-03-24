"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class StbImageHeader(Recipe):
    """
    Header-only version
    """
    name = "stb_image"
    version = "2.28"
    source_dir = "stb_image"
    kind = "header"
