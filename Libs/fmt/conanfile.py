from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.errors import ConanInvalidConfiguration


class fmtRecipe(ConanFile):
    name = "fmt"
    version = "9.1.0_owl"

    # Binary configuration
    settings = {"os", "compiler", "build_type", "arch"}
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    source_folder = "../../fmt-9.1.0"
    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "fmt-9.1.0/CMakeLists.txt", \
        "fmt-9.1.0/src/*", \
        "fmt-9.1.0/include/*", \
        "fmt-9.1.0/support/cmake/*", \
        "fmt-9.1.0/README.rst", \
        "fmt-9.1.0/ChangeLog.rst"

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
        tc.cache_variables["FMT_TEST"] = "OFF"
        tc.cache_variables["FMT_DOC"] = "OFF"
        tc.cache_variables["FMT_SYSTEM_HEADERS"] = "ON"
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
            self.cpp_info.libs = ["fmtd"]
        else:
            self.cpp_info.libs = ["fmt"]
