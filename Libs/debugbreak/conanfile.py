from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.errors import ConanInvalidConfiguration


class debugBreakRecipe(ConanFile):
    name = "debugbreak"
    version = "1.0_owl"

    exports_sources = "debugbreak-1.0/debugbreak.h", "debugbreak-config.cmake.in", "CMakeLists.txt"
    no_copy_source = True

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generator = "Ninja"
        tc.cache_variables["DBR_SYSTEM_HEADERS"] = "ON"
        tc.generate()

    def package(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.install(build_type="Release")

