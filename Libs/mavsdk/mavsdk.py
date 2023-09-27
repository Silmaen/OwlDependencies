"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe

ignore_list = ["SUPERBUILD",
               "BUILD_TESTS"]


class MavSDKShared(Recipe):
    """
    Shared version
    """
    name = "mavsdk"
    version = "1.4.17"
    source_dir = "MAVSDK"
    kind = "shared"
    dependencies = [{"name": "jsoncpp", "kind": kind},
                    {"name": "tinyxml2", "kind": kind}]

    def configure(self):
        for ignore in ignore_list:
            self.cache_variables[ignore] = "OFF"


class MavSDKStatic(Recipe):
    """
    Shared version
    """
    name = "mavsdk"
    version = "1.4.17"
    source_dir = "MAVSDK"
    kind = "static"
    dependencies = [{"name": "jsoncpp", "kind": kind},
                    {"name": "tinyxml2", "kind": kind}]

    def configure(self):
        for ignore in ignore_list:
            self.cache_variables[ignore] = "OFF"
