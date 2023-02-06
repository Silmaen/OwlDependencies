from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.errors import ConanInvalidConfiguration


class SpdlogRecipe(ConanFile):
    name = "glfw3"
    version = "3.3.8_owl"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    source_folder = "../../glfw-3.3.8"
    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "glfw-3.3.8/CMakeLists.txt", \
        "glfw-3.3.8/cmake_uninstall.cmake.in", \
        "glfw-3.3.8/src/*", \
        "glfw-3.3.8/include/*", \
        "glfw-3.3.8/CMake/*"

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
        tc.cache_variables["GLFW_BUILD_EXAMPLES"] = "OFF"
        tc.cache_variables["GLFW_BUILD_TESTS"] = "OFF"
        tc.cache_variables["GLFW_BUILD_DOCS"] = "OFF"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        if self.settings.os == "Windows" and self.options.shared:
            self.cpp_info.libs = ["glfw3dll"]
        else:
            self.cpp_info.libs = ["glfw3"]

    
