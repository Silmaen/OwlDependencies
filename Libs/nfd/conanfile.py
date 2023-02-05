from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.errors import ConanInvalidConfiguration


class nfdRecipe(ConanFile):
    name = "nfd"
    version = "1.0.1_owl"

    # Binary configuration
    settings = {"os", "compiler", "build_type", "arch"}
    options = {"shared": [True, False], "fPIC": [True, False], "Portal": [True, False]}
    default_options = {"shared": False, "fPIC": True, "Portal": False}

    source_folder = "../../nfd-1.0.1"
    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "nfd-1.0.1/CMakeLists.txt", \
        "nfd-1.0.1/src/*"

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
        if self.settings.os != "Linux":
            self.options.Portal = False

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generator = "Ninja"
        if self.options.shared:
            tc.cache_variables["BUILD_SHARED_LIBS"] = "ON"
        if self.options.Portal:
            tc.cache_variables["NFD_PORTAL"] = "ON"
        tc.cache_variables["NFD_BUILD_TESTS"] = "OFF"
        tc.cache_variables["NFD_INSTALL"] = "ON"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        if self.settings.build_type == "Debug":
            self.cpp_info.libs = ["nfdd"]
        else:
            self.cpp_info.libs = ["nfd"]
