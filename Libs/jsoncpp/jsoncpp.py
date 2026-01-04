"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe

ignore_list = [
    "JSONCPP_WITH_TESTS",
    "JSONCPP_WITH_POST_BUILD_UNITTEST",
    "BUILD_OBJECT_LIBS",
]
cmakelists_modif = ["jsoncppConfig.cmake.in"]
corrections = [
    [b"cmake_policy(PUSH)", b"#cmake_policy(PUSH)", None],
    [b"cmake_policy(VERSION 3.0)", b"#cmake_policy(VERSION 3.0)", None],
    [b"cmake_policy(POP)", b"#cmake_policy(POP)", None],
]


class JsonCppShared(Recipe):
    """
    Shared version
    """

    name = "jsoncpp"
    version = "1.9.6"
    source_dir = "jsoncpp"
    kind = "shared"
    description = "JsonCpp is a C++ library for interacting with JSON."

    def source(self):
        for cmakelists in cmakelists_modif:
            path = self.path / self.source_dir / cmakelists
            if not path.exists():
                print(f"Error: file {cmakelists} @ {path} not found...")
                continue
            with open(path, "rb") as fp:
                lines = fp.read()
            for correction in corrections:
                if correction[2] not in [None, ""]:
                    if correction[2] != cmakelists:
                        continue
                lines = lines.replace(correction[0], correction[1])
            with open(path, "wb") as fp:
                fp.write(lines)
            print(f"***** File {cmakelists} @ {path} found and modified.")

    def clean(self):
        for cmakelists in cmakelists_modif:
            path = self.path / self.source_dir / cmakelists
            if not path.exists():
                print(f"Error: file {cmakelists} @ {path} not found...")
                continue
            with open(path, "rb") as fp:
                lines = fp.read()
            for correction in corrections:
                if correction[2] not in [None, ""]:
                    if correction[2] != cmakelists:
                        continue
                lines = lines.replace(correction[1], correction[0])
                pass
            with open(path, "wb") as fp:
                fp.write(lines)
            print(f"***** File {cmakelists} @ {path} restored.")

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
