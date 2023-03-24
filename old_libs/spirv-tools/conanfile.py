from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.errors import ConanInvalidConfiguration


class spirvToolsRecipe(ConanFile):
    name = "spirv-tools"
    version = "2023.1_owl"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    source_folder = "../../src"
    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "src/CMakeLists.txt", \
        "src/CHANGES", \
        "src/cmake/*", \
        "src/source/*", \
        "src/utils/*", \
        "src/include/*", \
        "src/external/CMakeLists.txt", \
        "src/test/CMakeLists.txt", \
        "src/test/*/CMakeLists.txt", \
        "src/test/diff/diff_files/*.cmake", \
        "src/tools/CMakeLists.txt", \
        "src/tools/emacs/CMakeLists.txt", \
        "src/examples/CMakeLists.txt", \
        "src/examples/cpp-interface/CMakeLists.txt"

    def requirements(self):
        self.requires("spirv-headers/1.3.239_owl")

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
        tc.cache_variables["SPIRV_TOOLS_BUILD_STATIC"] = "OFF"
        tc.cache_variables["SPIRV_SKIP_EXECUTABLES"] = "ON"
        tc.cache_variables["SPIRV_SKIP_TESTS"] = "ON"
        tc.cache_variables["SPIRV-Headers_SOURCE_DIR"] = self.dependencies["spirv-headers"].package_folder
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["SPIRV-Tools", "SPIRV-Tools-diff", "SPIRV-Tools-link", "SPIRV-Tools-lint", "SPIRV-Tools-opt", "SPIRV-Tools-reduce", "SPIRV-Tools-shared"]
