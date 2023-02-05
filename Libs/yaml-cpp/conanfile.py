from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps


class YamlCppRecipe(ConanFile):
    name = "yaml-cpp"
    version = "0.7.0_owl"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    source_folder = "../../yaml-cpp-0.7.0"
    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "yaml-cpp-0.7.0/CMakeLists.txt", \
        "yaml-cpp-0.7.0/src/*", \
        "yaml-cpp-0.7.0/include/*", \
        "yaml-cpp-0.7.0/*.in"

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
        tc.cache_variables["YAML_CPP_BUILD_CONTRIB"] = "OFF"
        tc.cache_variables["YAML_CPP_BUILD_TOOLS"] = "OFF"
        tc.cache_variables["YAML_CPP_BUILD_TESTS"] = "OFF"
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
            self.cpp_info.libs = ["yaml-cppd"]
        else:
            self.cpp_info.libs = ["yaml-cpp"]

    
