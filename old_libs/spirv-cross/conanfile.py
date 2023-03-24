from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.errors import ConanInvalidConfiguration


class spirvCrossRecipe(ConanFile):
    name = "spirv-cross"
    version = "1.3.239_owl"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    source_folder = "../../src"
    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "src/CMakeLists.txt", \
        "src/cmake/*", \
        "src/pkg-config/*", \
        "src/*.cpp", \
        "src/*.hpp", \
        "src/*.h", \
        "src/include/*"

    def validate(self):
        if self.settings.os not in ["Windows", "Linux"]:
            raise ConanInvalidConfiguration(F" OS {self.settings.os} not supported")
        if self.settings.compiler not in ["gcc", "clang"]:
            raise ConanInvalidConfiguration(F"Compiler {self.settings.compiler} not supported")
        if self.settings.build_type not in ["Debug", "Release"]:
            raise ConanInvalidConfiguration(F"Build Type {self.settings.build_type} not supported")
        if self.settings.arch not in ["x86_64"]:
            raise ConanInvalidConfiguration(F"Arch {self.settings.arch} not supported")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
            self.options.shared = True

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generator = "Ninja"
        if self.options.shared:
            tc.cache_variables["SPIRV_CROSS_SHARED"] = "ON"
        tc.cache_variables["SPIRV_CROSS_ENABLE_TESTS"] = "OFF"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        if self.settings.os == "Windows" and self.settings.build_type == "Debug":
            self.cpp_info.libs = ["spirv-cross-cd", "spirv-cross-cored", "spirv-cross-cppd", "spirv-cross-c-sharedd", "spirv-cross-glsld","spirv-cross-hlsld","spirv-cross-msld", "spirv-cross-reflectd", "spirv-cross-utild"]
        else:
            self.cpp_info.libs = ["spirv-cross-c", "spirv-cross-core", "spirv-cross-cpp", "spirv-cross-c-shared", "spirv-cross-glsl", "spirv-cross-hlsl", "spirv-cross-msl", "spirv-cross-reflect", "spirv-cross-util"]
