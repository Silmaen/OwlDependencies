"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class SprivHeaderHeader(Recipe):
    """
    Shared version
    """
    name = "spirv-header"
    version = "1.3.243.0"
    source_dir = "SPIRV-Headers"
    kind = "header"

    def configure(self):
        self.cache_variables["SPIRV_HEADERS_SKIP_INSTALL"] = "OFF"
        self.cache_variables["SPIRV_HEADERS_SKIP_EXAMPLES"] = "ON"
