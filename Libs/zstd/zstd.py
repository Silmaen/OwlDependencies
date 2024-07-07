"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class ZstdShared(Recipe):
    """
    Shared version
    """

    name = "zstd"
    version = "1.5.6"
    source_dir = "sources/zstd/build/cmake"
    kind = "shared"

    def configure(self):
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"
        self.cache_variables["ZSTD_BUILD_PROGRAMS"] = "OFF"
        self.cache_variables["ZSTD_BUILD_TESTS"] = "OFF"
        self.cache_variables["ZSTD_PROGRAMS_LINK_SHARED"] = "ON"
        self.cache_variables["ZSTD_BUILD_STATIC"] = "OFF"
        self.cache_variables["ZSTD_BUILD_SHARED"] = "ON"


class ZstdStatic(ZstdShared):
    """
    Static version
    """

    kind = "static"

    def configure(self):
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"
        self.cache_variables["ZSTD_BUILD_PROGRAMS"] = "OFF"
        self.cache_variables["ZSTD_BUILD_TESTS"] = "OFF"
        self.cache_variables["ZSTD_PROGRAMS_LINK_SHARED"] = "ON"
        self.cache_variables["ZSTD_BUILD_STATIC"] = "ON"
        self.cache_variables["ZSTD_BUILD_SHARED"] = "OFF"
