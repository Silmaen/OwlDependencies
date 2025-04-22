"""
Depmanager recipes
"""

from pathlib import Path

from depmanager.api.recipe import Recipe

here = Path(__file__).parent


class OpenALShared(Recipe):
    """
    Shared version (the only one)
    """

    name = "openal"
    version = "1.24.3"
    source_dir = "openal-soft"
    kind = "shared"

    def configure(self):
        self.cache_variables["ALSOFT_EXAMPLES"] = "OFF"
        self.cache_variables["ALSOFT_INSTALL_EXAMPLES"] = "OFF"
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"
