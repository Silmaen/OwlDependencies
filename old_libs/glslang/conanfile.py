from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.errors import ConanInvalidConfiguration


class glslangRecipe(ConanFile):
    name = "glslang"
    version = "12.0.0_owl"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    source_folder = "../../src"
    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "src/CMakeLists.txt", \
        "src/*.cmake", \
        "src/CHANGES.md", \
        "src/build_info.h.tmpl", \
        "src/glslang/*", \
        "src/OGLCompilersDLL/*", \
        "src/SPIRV/*", \
        "src/StandAlone/*", \
        "src/hlsl/*", \
        "src/utils/*"

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
            tc.cache_variables["BUILD_SHARED_LIBS"] = "ON"
        tc.cache_variables["BUILD_EXTERNAL"] = "OFF"
        tc.cache_variables["ENABLE_SPVREMAPPER"] = "OFF"
        tc.cache_variables["ENABLE_GLSLANG_BINARIES"] = "OFF"
        tc.cache_variables["ENABLE_OPT"] = "OFF"
        tc.cache_variables["ENABLE_CTEST"] = "OFF"
        tc.cache_variables["ENABLE_HLSL"] = "ON"
        if self.settings.os == "Linux":
            tc.cache_variables["USE_CCACHE"] = "ON"
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
            self.cpp_info.libs = ["glslangd", "HLSLd", "SPIRVd", "OSDependentd"]
        else:
            self.cpp_info.libs = ["glslang", "HLSL", "SPIRV", "OSDependent"]

    
