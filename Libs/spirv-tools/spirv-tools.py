"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe
from depmanager.api.package import PackageManager

class SPIRVtoolsShared(Recipe):
    """
    Shared version
    """
    name = "spirv-tools"
    version = "1.3.243.0"
    source_dir = "SPIRV-Tools"
    kind = "shared"
    dependencies = [{"name": "spirv-header", "kind": "header"}]

    def configure(self):
        self.cache_variables["SPIRV_TOOLS_BUILD_STATIC"] = "OFF"
        self.cache_variables["SPIRV_SKIP_EXECUTABLES"] = "ON"
        self.cache_variables["SPIRV_SKIP_TESTS"] = "ON"
        pack = PackageManager()
        got = pack.query(self.dependencies[0], "")[0]
        self.cache_variables["SPIRV-Headers_SOURCE_DIR"] =str(got.get_path()).replace("\\", "/")


class SPIRVtoolsStatic(Recipe):
    """
    Shared version
    """
    name = "spirv-tools"
    version = "1.3.243.0"
    source_dir = "SPIRV-Tools"
    kind = "static"
    dependencies = [{"name": "spirv-header", "kind": "header"}]

    def configure(self):
        self.cache_variables["SPIRV_TOOLS_BUILD_STATIC"] = "ON"
        self.cache_variables["SPIRV_SKIP_EXECUTABLES"] = "ON"
        self.cache_variables["SPIRV_SKIP_TESTS"] = "ON"
        pack = PackageManager()
        got = pack.query(self.dependencies[0], "")[0]
        self.cache_variables["SPIRV-Headers_SOURCE_DIR"] =str(got.get_path()).replace("\\", "/")
