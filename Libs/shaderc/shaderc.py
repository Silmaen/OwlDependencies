"""
Depmanager recipes
"""
from pathlib import Path
from sys import executable

from depmanager.api.recipe import Recipe

here = Path(__file__).parent


class ShadercShared(Recipe):
    """
    Shared version
    """

    name = "shaderc"
    version = "1.3.275"
    source_dir = "sources"
    kind = "shared"

    def configure(self):
        self.cache_variables["SHADERC_SKIP_TESTS"] = "ON"
        self.cache_variables["SHADERC_SKIP_EXAMPLES"] = "ON"
        self.cache_variables["SHADERC_SKIP_COPYRIGHT_CHECK"] = "ON"
        self.cache_variables["ENABLE_GLSLANG_BINARIES"] = "OFF"
        self.cache_variables["ENABLE_SPVREMAPPER"] = "OFF"
        self.cache_variables["SPIRV_SKIP_EXECUTABLES"] = "ON"
        self.cache_variables["SPIRV_SKIP_TESTS"] = "ON"
        self.cache_variables["SPIRV_HEADERS_SKIP_EXAMPLES"] = "ON"
        self.cache_variables["SPIRV_TOOLS_BUILD_STATIC"] = "OFF"
        self.cache_variables["BUILD_SHARED_LIBS"] = "OFF"
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"
        self.cache_variables["PYTHON_EXECUTABLE"] = executable


class ShadercStatic(ShadercShared):
    """
    Any version
    """

    kind = "static"

    def configure(self):
        self.cache_variables["SHADERC_SKIP_TESTS"] = "ON"
        self.cache_variables["SHADERC_SKIP_EXAMPLES"] = "ON"
        self.cache_variables["SHADERC_SKIP_COPYRIGHT_CHECK"] = "ON"
        self.cache_variables["ENABLE_GLSLANG_BINARIES"] = "OFF"
        self.cache_variables["ENABLE_SPVREMAPPER"] = "OFF"
        self.cache_variables["SPIRV_SKIP_EXECUTABLES"] = "ON"
        self.cache_variables["SPIRV_SKIP_TESTS"] = "ON"
        self.cache_variables["SPIRV_HEADERS_SKIP_EXAMPLES"] = "ON"
        self.cache_variables["SPIRV_TOOLS_BUILD_STATIC"] = "ON"
        self.cache_variables["BUILD_SHARED_LIBS"] = "ON"
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"
        self.cache_variables["PYTHON_EXECUTABLE"] = executable
