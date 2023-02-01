from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps


class fmtRecipe(ConanFile):
    name = "fmt"
    version = "9.1.0_owl"

    # Optional metadata
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of fmt package here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "CMakeLists.txt", "src/*", "include/*", "support/cmake/*", "README.rst", "ChangeLog.rst"

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
        tc.generator = "Ninja Multi-Config"
        tc.cache_variables["FMT_TEST"] = "OFF"
        tc.cache_variables["FMT_DOC"] = "OFF"
        tc.cache_variables["FMT_SYSTEM_HEADERS"] = "ON"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build(build_type="Debug")
        cmake.build(build_type="Release")

    def package(self):
        cmake = CMake(self)
        cmake.install(build_type="Debug")
        cmake.install(build_type="Release")

    def package_info(self):
        self.cpp_info.libs = ["fmt"]

    
