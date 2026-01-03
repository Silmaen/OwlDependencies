"""
Depmanager recipes
"""

from pathlib import Path

from depmanager.api.recipe import Recipe

here = Path(__file__).parent


class MsdfAtlasGenShared(Recipe):
    """
    Shared version
    """

    name = "msdf-atlas-gen"
    version = "1.3"
    source_dir = "msdf-atlas-gen"
    kind = "shared"
    dependencies = [
        {"name": "msdfgen", "kind": "static"},
        {"name": "libpng", "kind": "static"},
    ]

    def configure(self):
        self.cache_variables["MSDF_ATLAS_BUILD_STANDALONE"] = "OFF"
        self.cache_variables["MSDF_ATLAS_USE_VCPKG"] = "OFF"
        self.cache_variables["MSDF_ATLAS_USE_SKIA"] = "OFF"
        self.cache_variables["MSDF_ATLAS_NO_ARTERY_FONT"] = "ON"
        self.cache_variables["MSDF_ATLAS_MSDFGEN_EXTERNAL"] = "ON"
        self.cache_variables["MSDF_ATLAS_INSTALL"] = "ON"
        self.cache_variables["CMAKE_DEBUG_POSTFIX"] = "d"


class MsdfAtlasGenStatic(MsdfAtlasGenShared):
    """
    Static version
    """

    kind = "static"
    dependencies = [
        {"name": "msdfgen", "kind": "static"},
        {"name": "libpng", "kind": "static"},
    ]

    def configure(self):
        super().configure()
