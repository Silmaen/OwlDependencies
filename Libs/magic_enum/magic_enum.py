"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class MagicEnumHeader(Recipe):
    """
    Header-only version
    """
    name = "magic_enum"
    version = "0.9.5"
    source_dir = "magic_enum"
    kind = "header"

    def configure(self):
        self.cache_variables["MAGIC_ENUM_OPT_BUILD_EXAMPLES"] = "OFF"
        self.cache_variables["MAGIC_ENUM_OPT_BUILD_TESTS"] = "OFF"
        self.cache_variables["MAGIC_ENUM_OPT_ENABLE_NONASCII"] = "ON"


