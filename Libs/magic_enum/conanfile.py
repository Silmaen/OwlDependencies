from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.errors import ConanInvalidConfiguration


class magicEnumRecipe(ConanFile):
    name = "magic_enum"
    version = "0.8.2_owl"

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "magic_enum-0.8.2/CMakeLists.txt", \
        "magic_enum-0.8.2/include/*", \
        "magic_enum-0.8.2/package.xml"
    source_folder = "magic_enum-0.8.2"

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generator = "Ninja"
        tc.cache_variables["MAGIC_ENUM_OPT_BUILD_EXAMPLES"] = "OFF"
        tc.cache_variables["MAGIC_ENUM_OPT_BUILD_TESTS"] = "OFF"
        tc.cache_variables["MAGIC_ENUM_OPT_ENABLE_NONASCII"] = "ON"
        tc.generate()

    def package(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.install(build_type="Release")
