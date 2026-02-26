"""
Depmanager recipes
"""

import subprocess

from depmanager.api.recipe import Recipe

# Sous-modules imbriqués de slang nécessaires au build.
# Initialisés automatiquement dans source() pour éviter un checkout récursif complet.
slang_required_submodules = [
    "external/lua",
    "external/unordered_dense",
    "external/miniz",
    "external/lz4",
]

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
    "slang/CMakeLists.txt",
    "slang/source/slang/CMakeLists.txt",
    "slang/source/slang-record-replay/util/record-utility.cpp",
    "slang/source/core/slang-secure-crt.h",
    "slang/source/slangc/main.cpp",
    "CMakeLists.txt",
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
    [
        b'@PACKAGE_INIT@\n        @INSTALL_CONFIG_UNIX@\n        include("@PACKAGE_PATH_EXPORT_TARGETS@")',
        b'@PACKAGE_INIT@\n        include(CMakeFindDependencyMacro)\n        find_dependency(SPIRV-Tools-opt)\n        @INSTALL_CONFIG_UNIX@\n        include("@PACKAGE_PATH_EXPORT_TARGETS@")',
        "CMakeLists.txt",
    ],
    [
        b"    find_package(SPIRV-Tools REQUIRED)",
        b"    #find_package(SPIRV-Tools REQUIRED)",
        "slang/CMakeLists.txt",
    ],
    [
        b"    find_package(glslang REQUIRED)",
        b"    #find_package(glslang REQUIRED)",
        "slang/CMakeLists.txt",
    ],
    [
        b"    add_library(glslang ALIAS glslang::glslang)",
        b"    #add_library(glslang ALIAS glslang::glslang)",
        "slang/CMakeLists.txt",
    ],
    [
        b"#ifdef _WIN32",
        b"#if defined(_WIN32) && !defined(__MINGW32__)",
        "slang/source/slang-record-replay/util/record-utility.cpp",
    ],
    [
        b"#ifndef _WIN32",
        b"#if defined(__MINGW32__) && !defined(SLANG_MINGW_FREAD_S_DEFINED)\n"
        b"#define SLANG_MINGW_FREAD_S_DEFINED\n"
        b"#include <assert.h>\n"
        b"#include <stdio.h>\n"
        b"inline size_t fread_s(void* buffer, [[maybe_unused]] size_t bufferSize,"
        b" size_t elementSize, size_t count, FILE* stream) {\n"
        b"    assert(bufferSize >= elementSize * count);\n"
        b"    return fread(buffer, elementSize, count, stream);\n"
        b"}\n"
        b"#endif\n"
        b"#ifndef _WIN32",
        "slang/source/core/slang-secure-crt.h",
    ],
    [
        b"#define MAIN slangc_main",
        b"#define MAIN main",
        "slang/source/slangc/main.cpp",
    ],
    [
        b'if(WIN32 AND SLANG_LIB_TYPE STREQUAL "SHARED")',
        b'if(MSVC AND SLANG_LIB_TYPE STREQUAL "SHARED")',
        "slang/source/slang/CMakeLists.txt",
    ],
]


class VulkanSdk(Recipe):
    """
    Shared version
    """

    name = "vulkan_sdk"
    version = "1.4.341"
    source_dir = "source"
    kind = "shared"
    config = ["Release"]

    def source(self):
        # Initialiser uniquement les sous-modules slang requis (pas de checkout récursif)
        slang_dir = self.path / self.source_dir / "slang"
        if (slang_dir / ".gitmodules").exists():
            subprocess.run(
                ["git", "submodule", "update", "--init"] + slang_required_submodules,
                cwd=str(slang_dir),
                check=True,
            )
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
