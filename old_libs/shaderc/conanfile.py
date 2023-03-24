from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.errors import ConanInvalidConfiguration


class shadercRecipe(ConanFile):
    name = "shaderc"
    version = "2023.2_owl"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # source_folder = "../../src"
    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "CMakeLists.txt", \
        "src/CMakeLists.txt", \
        "src/CHANGES", \
        "src/cmake/*", \
        "src/third_party/CMakeLists.txt", \
        "src/libshaderc_util/CMakeLists.txt", \
        "src/libshaderc_util/include/*", \
        "src/libshaderc_util/src/*", \
        "src/libshaderc/CMakeLists.txt", \
        "src/libshaderc/include/*", \
        "src/libshaderc/src/*", \
        "src/glslc/*"

    def requirements(self):
        self.requires("glslang/12.0.0_owl")
        self.requires("spirv-tools/2023.1_owl")

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
        tc.cache_variables["SHADERC_SKIP_TESTS"] = "ON"
        tc.cache_variables["SHADERC_SKIP_EXAMPLES"] = "ON"
        tc.cache_variables["SHADERC_SKIP_COPYRIGHT_CHECK"] = "ON"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["shaderc"]
