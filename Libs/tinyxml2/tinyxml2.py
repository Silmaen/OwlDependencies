"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe

ignore_list = ["BUILD_TESTING"]


class TinyXML2Shared(Recipe):
    """
    Shared version
    """

    name = "tinyxml2"
    version = "11.0.0"
    source_dir = "tinyxml2"
    kind = "shared"
    description = "TinyXML-2 is a simple, small, efficient, C++ XML parser"

    def configure(self):
        for ignore in ignore_list:
            self.cache_variables[ignore] = "OFF"


class TinyXML2Static(TinyXML2Shared):
    """
    Static version
    """

    kind = "static"
