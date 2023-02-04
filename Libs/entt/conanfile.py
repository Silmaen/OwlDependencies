from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.errors import ConanInvalidConfiguration


class enttRecipe(ConanFile):
    name = "entt"
    version = "3.11.1_owl"

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "entt-3.11.1/CMakeLists.txt", "entt-3.11.1/src/*", "entt-3.11.1/cmake/*"
    source_folder = "entt-3.11.1"

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generator = "Ninja"
        tc.cache_variables["ENTT_INCLUDE_HEADERS"] = "ON"
        tc.generate()

    def package(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.install(build_type="Release")
