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
    version = "9.0.0"
    source_dir = "tinyxml2"
    kind = "shared"

    def configure(self):
        for ignore in ignore_list:
            self.cache_variables[ignore] = "OFF"


class TinyXML2Static(Recipe):
    """
    Shared version
    """
    name = "tinyxml2"
    version = "9.0.0"
    source_dir = "tinyxml2"
    kind = "static"

    def configure(self):
        for ignore in ignore_list:
            self.cache_variables[ignore] = "OFF"
