"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class GoogleTestShared(Recipe):
    """
    Shared version
    """
    name = "googletest"
    version = "1.14.0"
    source_dir = "googletest"
    kind = "shared"

    def configure(self):
        self.cache_variables["BUILD_GMOCK"] = "OFF"
        self.cache_variables["INSTALL_GTEST"] = "ON"


class GoogleTestStatic(Recipe):
    """
    Shared version
    """
    name = "googletest"
    version = "1.14.0"
    source_dir = "googletest"
    kind = "static"

    def configure(self):
        self.cache_variables["BUILD_GMOCK"] = "OFF"
        self.cache_variables["INSTALL_GTEST"] = "ON"
