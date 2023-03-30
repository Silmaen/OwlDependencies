"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class ShadercShared(Recipe):
    """
    Shared version
    """
    name = "shaderc"
    version = "2023.3"
    source_dir = "sources"
    kind = "shared"
    dependencies = [{"name": "glslang", "kind": "shared"},
                    {"name": "spirv-tools", "kind": "shared"}]

    def configure(self):
        self.cache_variables["SPIRV_CROSS_SHARED"] = "ON"
        self.cache_variables["SHADERC_SKIP_TESTS"] = "ON"
        self.cache_variables["SHADERC_SKIP_EXAMPLES"] = "ON"
        self.cache_variables["SHADERC_SKIP_COPYRIGHT_CHECK"] = "ON"


class ShadercStatic(Recipe):
    """
    Shared version
    """
    name = "shaderc"
    version = "2023.3"
    source_dir = "sources"
    kind = "static"
    dependencies = [{"name": "glslang", "kind": "static"},
                    {"name": "spirv-tools", "kind": "shared"}]

    def configure(self):
        self.cache_variables["SHADERC_SKIP_TESTS"] = "ON"
        self.cache_variables["SHADERC_SKIP_EXAMPLES"] = "ON"
        self.cache_variables["SHADERC_SKIP_COPYRIGHT_CHECK"] = "ON"
