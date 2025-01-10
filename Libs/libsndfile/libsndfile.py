"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class LibSndFileShared(Recipe):
    """
    Shared version
    """

    name = "libsndfile"
    version = "1.2.2"
    source_dir = "libsndfile"
    kind = "shared"

    def configure(self):
        self.cache_variables["BUILD_TESTING"] = "OFF"
        self.cache_variables["INSTALL_PKGCONFIG_MODULE"] = "OFF"
        self.cache_variables["BUILD_EXAMPLES"] = "OFF"
        self.cache_variables["BUILD_PROGRAMS"] = "OFF"
        self.cache_variables["BUILD_REGTEST"] = "OFF"
        self.cache_variables["INSTALL_MANPAGES"] = "OFF"
        self.cache_variables["ENABLE_MPEG"] = "OFF"
        self.cache_variables["ENABLE_EXTERNAL_LIBS"] = "OFF"
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"


class LibSndFileStatic(LibSndFileShared):
    """
    Static version
    """

    kind = "static"
