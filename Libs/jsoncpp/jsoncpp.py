"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe

ignore_list = [
    "JSONCPP_WITH_TESTS",
    "JSONCPP_WITH_POST_BUILD_UNITTEST",
    "BUILD_OBJECT_LIBS",
]


class JsonCppShared(Recipe):
    """
    Shared version
    """

    name = "jsoncpp"
    version = "1.9.5"
    source_dir = "jsoncpp"
    kind = "shared"

    def configure(self):
        for ignore in ignore_list:
            self.cache_variables[ignore] = "OFF"
        self.cache_variables["BUILD_STATIC_LIBS"] = "OFF"
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"


class JsonCppStatic(JsonCppShared):
    """
    Static version
    """

    kind = "static"

    def configure(self):
        for ignore in ignore_list:
            self.cache_variables[ignore] = "OFF"
        self.cache_variables["BUILD_STATIC_LIBS"] = "ON"
        self.cache_variables["JSONCPP_WITH_CMAKE_PACKAGE"] = "ON"
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"
