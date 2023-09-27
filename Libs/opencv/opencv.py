"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe

ignore_list = ["WITH_OBSENSOR",
               "WITH_CPUFEATURES",
               "WITH_CAP_IOS",
               "WITH_CUDA",
               "WITH_NVCUVID",
               "WITH_NVCUVENC",
               "WITH_AVFOUNDATION",
               "WITH_WIN32UI",
               "WITH_DIRECTX",
               "WITH_OPENGL",
               "WITH_VULKAN",
               "WITH_OPENCL",
               "WITH_VTK",
               "WITH_GTK",
               "WITH_ITT",
               "WITH_OPENCLAMDFFT",
               "WITH_OPENCLAMDBLAS",
               "WITH_VA_INTEL",
               "WITH_1394",
               "BUILD_JAVA",
               "BUILD_PERF_TESTS",
               "BUILD_TESTS",
               "BUILD_opencv_apps",
               "CV_TRACE"]


class OpenCVShared(Recipe):
    """
    Shared version
    """
    name = "opencv"
    version = "4.8.0"
    source_dir = "opencv"
    kind = "shared"

    def configure(self):
        for ignore in ignore_list:
            self.cache_variables[ignore] = "OFF"
        self.cache_variables["INSTALL_CREATE_DISTRIB"] = "ON"
        if self.settings["os"] == "Windows":
            self.cache_variables["CMAKE_CXX_FLAGS"] = "-Wa,-mbig-obj"
            self.cache_variables["CMAKE_EXE_LINKER_FLAGS"] = "-Wa,-mbig-obj"


class OpenCVStatic(Recipe):
    """
    Shared version
    """
    name = "opencv"
    version = "4.8.0"
    source_dir = "opencv"
    kind = "static"

    def configure(self):
        for ignore in ignore_list:
            self.cache_variables[ignore] = "OFF"
        self.cache_variables["INSTALL_CREATE_DISTRIB"] = "ON"
        if self.settings["os"] == "Windows":
            self.cache_variables["CMAKE_CXX_FLAGS"] = "-Wa,-mbig-obj"
            self.cache_variables["CMAKE_EXE_LINKER_FLAGS"] = "-Wa,-mbig-obj"
