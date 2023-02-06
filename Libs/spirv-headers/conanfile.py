from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.errors import ConanInvalidConfiguration


class spirvHeadersRecipe(ConanFile):
    name = "spirv-headers"
    version = "1.3.239_owl"

    exports_sources = "src/CMakeLists.txt", \
        "src/cmake/*", \
        "src/source/*", \
        "src/include/*", \
        "src/*.in"
    source_folder = "src"

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generator = "Ninja"
        tc.cache_variables["SPIRV_HEADERS_SKIP_INSTALL"] = "OFF"
        tc.cache_variables["SPIRV_HEADERS_SKIP_EXAMPLES"] = "ON"
        tc.generate()

    def package(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.install(build_type="Release")
