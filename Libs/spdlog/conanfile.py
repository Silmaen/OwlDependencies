from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps


class SpdlogRecipe(ConanFile):
    name = "spdlog"
    version = "1.11.0_owl"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    source_folder = "../../spdlog-1.11.0"
    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "spdlog-1.11.0/CMakeLists.txt", \
        "spdlog-1.11.0/src/*", \
        "spdlog-1.11.0/include/*", \
        "spdlog-1.11.0/cmake/*"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
            self.options.shared = True

    def requirements(self):
        self.requires("fmt/9.1.0_owl")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generator = "Ninja"
        if self.options.shared:
            tc.cache_variables["SPDLOG_BUILD_SHARED"] = "ON"
        else:
            if self.options.fPIC:
                tc.cache_variables["SPDLOG_BUILD_PIC"] = "ON"
        tc.cache_variables["SPDLOG_BUILD_EXAMPLE"] = "OFF"
        tc.cache_variables["SPDLOG_BUILD_TESTS"] = "OFF"
        tc.cache_variables["SPDLOG_BUILD_BENCH"] = "OFF"
        tc.cache_variables["SPDLOG_FMT_EXTERNAL"] = "ON"
        if self.settings.os == "Windows":
            tc.cache_variables["SPDLOG_WCHAR_SUPPORT"] = "ON"
            tc.cache_variables["SPDLOG_WCHAR_FILENAMES"] = "ON"
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
            self.cpp_info.libs = ["spdlogd"]
        else:
            self.cpp_info.libs = ["spdlog"]

    
