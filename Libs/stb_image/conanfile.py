from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.errors import ConanInvalidConfiguration


class stbImageRecipe(ConanFile):
    name = "stb-image"
    version = "2.28_owl"

    exports_sources = "stb_image-2.28/stb_image.h", "stb_image-config.cmake.in", "CMakeLists.txt"
    no_copy_source = True

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generator = "Ninja"
        tc.cache_variables["STB_SYSTEM_HEADERS"] = "ON"
        tc.generate()

    def package(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.install(build_type="Release")

