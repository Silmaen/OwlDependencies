"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe


class YamlCppShared(Recipe):
    """
    Shared version
    """
    name = "yaml-cpp"
    version = "0.8.0"
    source_dir = "yaml-cpp"
    kind = "shared"

    def configure(self):
        self.cache_variables["YAML_CPP_BUILD_CONTRIB"] = "OFF"
        self.cache_variables["YAML_CPP_BUILD_TOOLS"] = "OFF"
        self.cache_variables["YAML_CPP_BUILD_TESTS"] = "OFF"


class YamlCppStatic(Recipe):
    """
    Shared version
    """
    name = "yaml-cpp"
    version = "0.8.0"
    source_dir = "yaml-cpp"
    kind = "static"

    def configure(self):
        self.cache_variables["YAML_CPP_BUILD_CONTRIB"] = "OFF"
        self.cache_variables["YAML_CPP_BUILD_TOOLS"] = "OFF"
        self.cache_variables["YAML_CPP_BUILD_TESTS"] = "OFF"
