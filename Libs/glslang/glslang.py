"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class GlslangShared(Recipe):
    """
    Shared version
    """
    name = "glslang"
    version = "1.11.0"
    source_dir = "glslang"
    kind = "shared"

    def configure(self):
        self.cache_variables["BUILD_EXTERNAL"] = "OFF"
        self.cache_variables["ENABLE_SPVREMAPPER"] = "OFF"
        self.cache_variables["ENABLE_GLSLANG_BINARIES"] = "OFF"
        self.cache_variables["ENABLE_OPT"] = "OFF"
        self.cache_variables["ENABLE_CTEST"] = "OFF"
        self.cache_variables["ENABLE_HLSL"] = "ON"


class GlslangStatic(Recipe):
    """
    Shared version
    """
    name = "glslang"
    version = "1.11.0"
    source_dir = "glslang"
    kind = "static"

    def configure(self):
        self.cache_variables["BUILD_EXTERNAL"] = "OFF"
        self.cache_variables["ENABLE_SPVREMAPPER"] = "OFF"
        self.cache_variables["ENABLE_GLSLANG_BINARIES"] = "OFF"
        self.cache_variables["ENABLE_OPT"] = "OFF"
        self.cache_variables["ENABLE_CTEST"] = "OFF"
        self.cache_variables["ENABLE_HLSL"] = "ON"
