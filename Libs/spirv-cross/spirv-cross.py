"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class SPIRVCrossShared(Recipe):
    """
    Shared version
    """
    name = "spirv-cross"
    version = "1.3.239.0"
    source_dir = "SPIRV-Cross"
    kind = "shared"

    def configure(self):
        self.cache_variables["SPIRV_CROSS_SHARED"] = "ON"
        self.cache_variables["SPIRV_CROSS_ENABLE_TESTS"] = "OFF"


class SPIRVCrossStatic(Recipe):
    """
    Shared version
    """
    name = "spirv-cross"
    version = "1.3.239.0"
    source_dir = "SPIRV-Cross"
    kind = "static"

    def configure(self):
        self.cache_variables["SPIRV_CROSS_ENABLE_TESTS"] = "OFF"
