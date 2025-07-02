"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class GoogleTestShared(Recipe):
    """
    Shared version
    """

    name = "googletest"
    version = "1.17.0"
    source_dir = "googletest"
    kind = "shared"

    def configure(self):
        self.cache_variables["BUILD_GMOCK"] = "OFF"
        self.cache_variables["INSTALL_GTEST"] = "ON"
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"


class GoogleTestStatic(GoogleTestShared):
    """
    Static version
    """

    kind = "static"
