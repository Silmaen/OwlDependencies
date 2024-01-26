"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe

ignore_list = ["BUILD_TESTING"]

cmakelists_modif = [
    "Vulkan-ValidationLayers/CMakeLists.txt",
    "Vulkan-ExtensionLayer/CMakeLists.txt",
    "shaderc/libshaderc/CMakeLists.txt",
    "shaderc/libshaderc_util/CMakeLists.txt"
]


class VulkanSdk(Recipe):
    """
    Shared version
    """

    name = "vulkan_sdk"
    version = "1.3.275"
    source_dir = "source"
    kind = "shared"
    config = ["Release"]

    def source(self):
        for cmakelists in cmakelists_modif:
            path = self.path / self.source_dir / cmakelists
            if not path.exists():
                print(f"Error: file {cmakelists} @ {path} not found...")
                continue
            with open(path, "rb") as fp:
                lines = fp.read()
            lines = lines.replace(b"\nfind_package", b"\n#find_package")
            lines = lines.replace(b"PUBLIC include", b"PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include> $<INSTALL_INTERFACE:include>")
            with open(path, "wb") as fp:
                fp.write(lines)
            print(f"***** File {cmakelists} @ {path} found and modified.")

    def clean(self):
        for cmakelists in cmakelists_modif:
            path = self.path / self.source_dir / cmakelists
            if not path.exists():
                print(f"Error: file {cmakelists} @ {path} not found...")
                continue
            with open(path, "rb") as fp:
                lines = fp.read()
            lines = lines.replace(b"\n#find_package", b"\nfind_package")
            lines = lines.replace(b"PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include> $<INSTALL_INTERFACE:include>", b"PUBLIC include")
            with open(path, "wb") as fp:
                fp.write(lines)
            print(f"***** File {cmakelists} @ {path} restored.")

    def configure(self):
        self.cache_variables["VK_VERSION_STRING"] = f"{self.version}"
        self.cache_variables["PYTHON_EXECUTABLE"] = "python3"
        if self.settings["os"] == "Windows":
            self.cache_variables["BUILD_DLL_VERSIONINFO"] = f"{self.version}"
