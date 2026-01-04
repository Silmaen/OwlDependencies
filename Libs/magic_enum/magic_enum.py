"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class MagicEnumHeader(Recipe):
    """
    Header-only version
    """

    name = "magic_enum"
    version = "0.9.7"
    source_dir = "magic_enum"
    kind = "header"
    description = "Magic Enum is a header-only C++17 library for reflection of enums"

    def configure(self):
        self.cache_variables["MAGIC_ENUM_OPT_BUILD_EXAMPLES"] = "OFF"
        self.cache_variables["MAGIC_ENUM_OPT_BUILD_TESTS"] = "OFF"
        self.cache_variables["MAGIC_ENUM_OPT_ENABLE_NONASCII"] = "ON"
