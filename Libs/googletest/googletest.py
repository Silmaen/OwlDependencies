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
    description = "GoogleTest is a unit testing library for the C++ programming language, based on the xUnit architecture."

    def configure(self):
        self.cache_variables["BUILD_GMOCK"] = "OFF"
        self.cache_variables["INSTALL_GTEST"] = "ON"
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"


class GoogleTestStatic(GoogleTestShared):
    """
    Static version
    """

    kind = "static"
