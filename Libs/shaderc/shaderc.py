"""
Depmanager recipes
"""
from shutil import copyfile, rmtree

from depmanager.api.recipe import Recipe
from tempfile import gettempdir
from pathlib import Path

here = Path(__file__).parent


class Shaderc(Recipe):
    """
    Any version
    """
    name = "shaderc"
    version = "2023.3"
    source_dir = "sources"
    kind = "any"

    def __init__(self):
        self.backupFiles = {}

    def configure(self):
        self.cache_variables["SHADERC_SKIP_TESTS"] = "ON"
        self.cache_variables["SHADERC_SKIP_EXAMPLES"] = "ON"
        self.cache_variables["SHADERC_SKIP_COPYRIGHT_CHECK"] = "ON"
        self.cache_variables["ENABLE_GLSLANG_BINARIES"] = "OFF"
        self.cache_variables["ENABLE_SPVREMAPPER"] = "OFF"
        self.cache_variables["ENABLE_CTEST"] = "OFF"
        self.cache_variables["SPIRV_SKIP_EXECUTABLES"] = "ON"
        self.cache_variables["SPIRV_SKIP_TESTS"] = "ON"
        self.cache_variables["SPIRV_HEADERS_SKIP_EXAMPLES"] = "ON"
        self.cache_variables["SPIRV_TOOLS_BUILD_STATIC"] = "OFF"
        self.cache_variables["BUILD_SHARED_LIBS"] = "OFF"
        self.cache_variables["BUILD_TESTING"] = "OFF"

    def source(self):
        """
        Done at the beginning of the procedure
        """
        temp = Path(gettempdir()) / "depbuilder"
        temp.mkdir(exist_ok=True, parents=True)
        source = here / Path(self.source_dir)
        # SPIRV Tools add-in
        copyfile(source / "SPIRV-Tools" / "CMakeLists.txt", temp / "CMakeLists_spirv-tools.txt")
        with open(source / "SPIRV-Tools" / "CMakeLists.txt", "a") as fp:
            fp.write('if (WIN32)\n')
            fp.write('  set(CMAKE_DEBUG_POSTFIX "d")\n')
            fp.write('endif ()\n')
        # shaderc
        copyfile(source / "shaderc" / "cmake" / "utils.cmake", temp / "shaderc_utils.cmake")
        copyfile(source / "modif_shaderc" / "cmake" / "utils.cmake", source / "shaderc" / "cmake" / "utils.cmake")
        copyfile(source / "shaderc" / "glslc" / "CMakeLists.txt", temp / "glslc_CMakeLists.txt")
        copyfile(source / "modif_shaderc" / "glslc" / "CMakeLists.txt", source / "shaderc" / "glslc" / "CMakeLists.txt")
        copyfile(source / "shaderc" / "libshaderc" / "CMakeLists.txt", temp / "libshaderc_CMakeLists.txt")
        copyfile(source / "modif_shaderc" / "libshaderc" / "CMakeLists.txt", source / "shaderc" / "libshaderc" / "CMakeLists.txt")
        copyfile(source / "shaderc" / "libshaderc_util" / "CMakeLists.txt", temp / "libshaderc_util_CMakeLists.txt")
        copyfile(source / "modif_shaderc" / "libshaderc_util" / "CMakeLists.txt", source / "shaderc" / "libshaderc_util" / "CMakeLists.txt")
        copyfile(source / "shaderc" / "CMakeLists.txt", temp / "shaderc_CMakeLists.txt")
        copyfile(source / "modif_shaderc" / "CMakeLists.txt", source / "shaderc" / "CMakeLists.txt")

    def clean(self):
        """
        Done at the end
        """
        temp = Path(gettempdir()) / "depbuilder"
        source = here / Path(self.source_dir)
        # Restore SPIRV
        copyfile(temp / "CMakeLists_spirv-tools.txt", source / "SPIRV-Tools" / "CMakeLists.txt")
        # shaderc
        copyfile(temp / "shaderc_utils.cmake", source / "shaderc" / "cmake" / "utils.cmake")
        copyfile(temp / "glslc_CMakeLists.txt", source / "shaderc" / "glslc" / "CMakeLists.txt")
        copyfile(temp / "libshaderc_CMakeLists.txt", source / "shaderc" / "libshaderc" / "CMakeLists.txt")
        copyfile(temp / "libshaderc_util_CMakeLists.txt", source / "shaderc" / "libshaderc_util" / "CMakeLists.txt")
        copyfile(temp / "shaderc_CMakeLists.txt", source / "shaderc" / "CMakeLists.txt")

        rmtree(temp)
