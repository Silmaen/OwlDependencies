"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class NfdShared(Recipe):
    """
    Shared version
    """
    name = "nfd"
    version = "1.0.2"
    source_dir = "nativefiledialog-extended"
    kind = "shared"

    def configure(self):
        self.cache_variables["NFD_BUILD_TESTS"] = "OFF"
        self.cache_variables["NFD_INSTALL"] = "ON"


class NfdStatic(Recipe):
    """
    Shared version
    """
    name = "nfd"
    version = "1.0.2"
    source_dir = "nativefiledialog-extended"
    kind = "static"

    def configure(self):
        self.cache_variables["NFD_BUILD_TESTS"] = "OFF"
        self.cache_variables["NFD_INSTALL"] = "ON"

