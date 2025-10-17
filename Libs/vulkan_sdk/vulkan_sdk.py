"""
Depmanager recipes
"""

from depmanager.api.recipe import Recipe

ignore_list = ["BUILD_TESTING"]

cmakelists_modif = [
    "Vulkan-Loader/loader/CMakeLists.txt",
    "Vulkan-Loader/CMakeLists.txt",
    "Vulkan-Utility-Libraries/CMakeLists.txt",
    "SPIRV-Headers/CMakeLists.txt",
    "SPIRV-Tools/CMakeLists.txt",
    "Vulkan-ValidationLayers/CMakeLists.txt",
    "Vulkan-ExtensionLayer/CMakeLists.txt",
    "SPIRV-Cross/CMakeLists.txt",
    "SPIRV-Reflect/CMakeLists.txt",
    "shaderc/libshaderc/CMakeLists.txt",
    "shaderc/libshaderc_util/CMakeLists.txt",
]

corrections = [
    [b"\nfind_package(VulkanHeaders", b"\n#find_package(VulkanHeaders", None],
    [
        b"\nfind_package(VulkanUtilityLibraries",
        b"\n#find_package(VulkanUtilityLibraries",
        None,
    ],
    [b"\nfind_package(SPIRV-Headers", b"\n#find_package(SPIRV-Headers", None],
    [b"\nfind_package(SPIRV-Tools-opt", b"\n#find_package(SPIRV-Tools-opt", None],
    [
        b"${CMAKE_INSTALL_LIBDIR}/cmake/VulkanLoader",
        b'"${cmake_install_dir}"',
        "Vulkan-Loader/loader/CMakeLists.txt",
    ],
    [
        b"PUBLIC include",
        b"PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include> $<INSTALL_INTERFACE:include>",
        None,
    ],
    [b"${CMAKE_INSTALL_DATADIR}/pkgconfig", b"${cmake_install_dir}/pkgconfig", None],
    [b"set(${PATH} ${TARGET}/cmake)", b"set(${PATH} ${cmake_install_dir})", None],
    [
        b"set(${PATH} ${CMAKE_INSTALL_LIBDIR}/cmake/${TARGET})",
        b"set(${PATH} ${cmake_install_dir} )",
        None,
    ],
    [
        b"EXPORT ${config_name}Config DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/${config_name}/cmake",
        b"EXPORT ${config_name}Config DESTINATION ${cmake_install_dir}",
        None,
    ],
]


class VulkanSdk(Recipe):
    """
    Shared version
    """

    name = "vulkan_sdk"
    version = "1.4.328"
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
            for correction in corrections:
                if correction[2] not in [None, ""]:
                    if correction[2] != cmakelists:
                        continue
                lines = lines.replace(correction[0], correction[1])
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
            for correction in corrections:
                if correction[2] not in [None, ""]:
                    if correction[2] != cmakelists:
                        continue
                lines = lines.replace(correction[1], correction[0])
                pass
            with open(path, "wb") as fp:
                fp.write(lines)
            print(f"***** File {cmakelists} @ {path} restored.")

    def configure(self):
        self.cache_variables["VK_VERSION_STRING"] = f"{self.version}"
        self.cache_variables["PYTHON_EXECUTABLE"] = "python3"
        if self.settings["os"] == "Windows":
            self.cache_variables["BUILD_DLL_VERSIONINFO"] = f"{self.version}"
