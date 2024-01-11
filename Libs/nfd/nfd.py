"""
Depmanager recipes
"""
from shutil import copyfile
from tempfile import gettempdir
from depmanager.api.recipe import Recipe
from pathlib import Path

here = Path(__file__).parent


class NfdShared(Recipe):
    """
    Shared version
    """
    name = "nfd"
    version = "1.1.1"
    source_dir = "nativefiledialog-extended"
    kind = "shared"

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
        self.cache_variables["NFD_BUILD_TESTS"] = "OFF"
        self.cache_variables["NFD_INSTALL"] = "ON"
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"

