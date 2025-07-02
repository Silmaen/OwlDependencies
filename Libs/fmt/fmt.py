"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class FmtShared(Recipe):
    """
    Shared version
    """

    name = "fmt"
    version = "11.2.0"
    source_dir = "fmt"
    kind = "shared"

    def configure(self):
        self.cache_variables["FMT_TEST"] = "OFF"
        self.cache_variables["FMT_DOC"] = "OFF"
        self.cache_variables["FMT_SYSTEM_HEADERS"] = "ON"


class FmtStatic(FmtShared):
    """
    Static version
    """

    kind = "static"
