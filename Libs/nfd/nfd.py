"""
Depmanager recipes
"""

from pathlib import Path

from depmanager.api.recipe import Recipe

here = Path(__file__).parent


class NfdShared(Recipe):
    """
    Shared version
    """

    name = "nfd"
    version = "1.2.1"
    source_dir = "nativefiledialog-extended"
    kind = "shared"
    description = "Native File Dialog Extended is a tiny, neat C/C++ library that portably invokes native file open/save dialogs"

    def configure(self):
        self.cache_variables["NFD_BUILD_TESTS"] = "OFF"
        self.cache_variables["NFD_INSTALL"] = "ON"
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"


class NfdStatic(NfdShared):
    """
    Static version
    """

    kind = "static"

    def configure(self):
        super().configure()
