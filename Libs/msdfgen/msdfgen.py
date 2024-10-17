"""
Depmanager recipes
"""

from pathlib import Path

from depmanager.api.recipe import Recipe

here = Path(__file__).parent


class MsdfGenShared(Recipe):
    """
    Shared version
    """

    name = "msdfgen"
    version = "1.12"
    source_dir = "msdfgen"
    kind = "shared"
    dependencies = [
        {"name": "tinyxml2", "kind": "shared"},
    ]

    def configure(self):
        self.cache_variables["MSDFGEN_BUILD_STANDALONE"] = "OFF"
        self.cache_variables["MSDFGEN_INSTALL"] = "ON"
        self.cache_variables["MSDFGEN_USE_VCPKG"] = "OFF"
        self.cache_variables["MSDFGEN_USE_SKIA"] = "OFF"
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"


class MsdfGenStatic(MsdfGenShared):
    """
    Static version
    """

    kind = "static"
    dependencies = [
        {"name": "tinyxml2", "kind": "static"},
    ]

    def configure(self):
        self.cache_variables["MSDFGEN_BUILD_STANDALONE"] = "OFF"
        self.cache_variables["MSDFGEN_INSTALL"] = "ON"
        self.cache_variables["MSDFGEN_USE_VCPKG"] = "OFF"
        self.cache_variables["MSDFGEN_USE_SKIA"] = "OFF"
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"
