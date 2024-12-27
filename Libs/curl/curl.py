"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class CurlShared(Recipe):
    """
    Shared version
    """

    name = "curl"
    version = "8.11.1"
    source_dir = "curl"
    kind = "shared"

    def configure(self):
        self.cache_variables["BUILD_CURL_EXE"] = "OFF"
        self.cache_variables["BUILD_STATIC_LIBS"] = "OFF"
        self.cache_variables["BUILD_SHARED_LIBS"] = "ON"


class CurlStatic(CurlShared):
    """
    Static version
    """

    kind = "static"

    def configure(self):
        self.cache_variables["BUILD_CURL_EXE"] = "OFF"
        self.cache_variables["BUILD_STATIC_LIBS"] = "ON"
        self.cache_variables["BUILD_SHARED_LIBS"] = "OFF"
