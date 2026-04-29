"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class Md4cShared(Recipe):
    """
    Shared version
    """

    name = "md4c"
    version = "0.5.2"
    source_dir = "md4c"
    kind = "shared"
    description = "C99 CommonMark parser with GFM extensions (tables, fenced code, autolinks)."

    def configure(self):
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"
        self.cache_variables["BUILD_MD2HTML_EXECUTABLE"] = "OFF"
        self.cache_variables["BUILD_SHARED_LIBS"] = "ON"


class Md4cStatic(Md4cShared):
    """
    Static version
    """

    kind = "static"

    def configure(self):
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"
        self.cache_variables["BUILD_MD2HTML_EXECUTABLE"] = "OFF"
        self.cache_variables["BUILD_SHARED_LIBS"] = "OFF"
        self.cache_variables["CMAKE_POSITION_INDEPENDENT_CODE"] = "ON"
