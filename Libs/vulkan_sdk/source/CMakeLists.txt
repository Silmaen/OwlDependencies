cmake_minimum_required(VERSION 3.17.2)

if (NOT VK_VERSION_STRING)
    set(VK_VERSION_STRING 1.3.275)
endif ()

project(VulkanSDK VERSION ${VK_VERSION_STRING})

include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

set(cmake_install_dir "${CMAKE_INSTALL_LIBDIR}/cmake")
set(cmake_full_install_dir "${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_LIBDIR}/cmake")
option(SDK_INSTALL "If we should install the Vulkan-SDK" ON)

function(dump_cmake_variables)
    get_cmake_property(_variableNames VARIABLES)
    list(SORT _variableNames)
    foreach (_variableName ${_variableNames})
        if (ARGV0)
            unset(MATCHED)
            string(REGEX MATCH ${ARGV0} MATCHED ${_variableName})
            if (NOT MATCHED)
                continue()
            endif ()
        endif ()
        message(STATUS "${_variableName}=${${_variableName}}")
    endforeach ()
endfunction()

# =========== Vulkan-Headers ================================
# headers part...
add_subdirectory(Vulkan-Headers)

if (SDK_INSTALL)
    set(VULKAN_HEADERS_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/Vulkan-Headers")
    set(VULKAN_HEADERS_BINARY_DIR "${CMAKE_CURRENT_BINARY_DIR}/Vulkan-Headers")

    install(DIRECTORY "${VULKAN_HEADERS_SOURCE_DIR}/include/vk_video" DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
    install(DIRECTORY "${VULKAN_HEADERS_SOURCE_DIR}/include/vulkan" DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
    # Preserve source permissions https://github.com/KhronosGroup/Vulkan-Headers/issues/336
    install(DIRECTORY "${VULKAN_HEADERS_SOURCE_DIR}/registry" DESTINATION "${CMAKE_INSTALL_DATADIR}/vulkan" USE_SOURCE_PERMISSIONS)

    set_target_properties(Vulkan-Headers PROPERTIES EXPORT_NAME "Headers")
    install(TARGETS Vulkan-Headers EXPORT VulkanHeadersConfig INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
    install(EXPORT VulkanHeadersConfig NAMESPACE "Vulkan::" DESTINATION "${cmake_install_dir}")

    set(version_config "${VULKAN_HEADERS_BINARY_DIR}/generated/VulkanHeadersConfigVersion.cmake")
    write_basic_package_version_file("${version_config}" COMPATIBILITY SameMajorVersion ARCH_INDEPENDENT)
    install(FILES "${version_config}" DESTINATION "${cmake_install_dir}")
    set(VULKAN_HEADERS_INSTALL_DIR "${cmake_full_install_dir}")
endif ()
message(STATUS "-- -- Vulkan-Headers Configured")
# =========== Vulkan-Headers ================================

# ============ Vulkan-Loader ================================
add_subdirectory(Vulkan-Loader)
set(VULKAN_LOADER_INSTALL_DIR "${cmake_full_install_dir}")
message(STATUS "-- -- Vulkan-Loader Configured")
# ============ Vulkan-Loader ================================

# ======= Vulkan-Utility-Libraries ==========================
add_subdirectory(Vulkan-Utility-Libraries)

if (SDK_INSTALL)
    set(VULKAN_UL_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/Vulkan-Utility-Libraries")
    set(VULKAN_UL_BINARY_DIR "${CMAKE_CURRENT_BINARY_DIR}/Vulkan-Utility-Libraries")

    install(
            DIRECTORY "${VULKAN_UL_SOURCE_DIR}/include/${API_TYPE}/"
            DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}/vulkan"
    )

    # Create VulkanUtilityLibraries-targets.cmake
    set_target_properties(VulkanLayerSettings PROPERTIES EXPORT_NAME "LayerSettings")
    set_target_properties(VulkanUtilityHeaders PROPERTIES EXPORT_NAME "UtilityHeaders")
    set_target_properties(VulkanCompilerConfiguration PROPERTIES EXPORT_NAME "CompilerConfiguration")
    install(
            TARGETS VulkanLayerSettings VulkanUtilityHeaders VulkanCompilerConfiguration
            EXPORT VulkanUtilityLibraries-targets
            INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
    )
    install(
            EXPORT VulkanUtilityLibraries-targets
            DESTINATION "${cmake_install_dir}"
            NAMESPACE Vulkan::
    )

    # Create VulkanUtilityLibrariesConfig.cmake
    set(VUL_EXPORT_TARGETS "${cmake_install_dir}/VulkanUtilityLibraries-targets.cmake")
    file(WRITE "${VULKAN_UL_BINARY_DIR}/VulkanUtilityLibrariesConfig.cmake.in" [=[
        include(CMakeFindDependencyMacro)
        # NOTE: Because VulkanHeaders is a PUBLIC dependency it needs to be found prior to VulkanUtilityLibraries
        find_dependency(VulkanHeaders REQUIRED)

        @PACKAGE_INIT@

        include(@PACKAGE_VUL_EXPORT_TARGETS@)
    ]=])

    configure_package_config_file(
            ${VULKAN_UL_BINARY_DIR}/VulkanUtilityLibrariesConfig.cmake.in
            ${VULKAN_UL_BINARY_DIR}/VulkanUtilityLibrariesConfig.cmake
            INSTALL_DESTINATION "${cmake_install_dir}"
            PATH_VARS VUL_EXPORT_TARGETS
            NO_SET_AND_CHECK_MACRO
            NO_CHECK_REQUIRED_COMPONENTS_MACRO
    )

    install(FILES ${VULKAN_UL_BINARY_DIR}/VulkanUtilityLibrariesConfig.cmake
            DESTINATION "${cmake_install_dir}"
    )
    set(VULKAN_UTILITY_LIBRARIES_INSTALL_DIR "${cmake_full_install_dir}")
endif ()
message(STATUS "-- -- Vulkan-Utility-Libraries")
# ======= Vulkan-Utility-Libraries ==========================

# ============ SPIRV-Headers ================================
add_subdirectory(SPIRV-Headers)

if (SDK_INSTALL)
    set(SPIRV_HEADERS_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/SPIRV-Headers")
    set(SPIRV_HEADERS_BINARY_DIR "${CMAKE_CURRENT_BINARY_DIR}/SPIRV-Headers")

    install(DIRECTORY ${SPIRV_HEADERS_SOURCE_DIR}/include/spirv DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

    set(version_config "${SPIRV_HEADERS_BINARY_DIR}/generated/SPIRV-HeadersConfigVersion.cmake")

    write_basic_package_version_file("${version_config}" COMPATIBILITY SameMajorVersion ARCH_INDEPENDENT)
    install(FILES "${version_config}" DESTINATION "${cmake_install_dir}")

    install(TARGETS SPIRV-Headers EXPORT "SPIRV-HeadersConfig" INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
    install(EXPORT "SPIRV-HeadersConfig" NAMESPACE "SPIRV-Headers::" DESTINATION "${cmake_install_dir}")

    if (IS_ABSOLUTE ${CMAKE_INSTALL_INCLUDEDIR})
        set(SPIRV_HEADERS_PKGCONFIG_INCLUDE_DIR ${CMAKE_INSTALL_INCLUDEDIR})
    else ()
        set(SPIRV_HEADERS_PKGCONFIG_INCLUDE_DIR ${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_INCLUDEDIR})
    endif ()
    configure_file(${SPIRV_HEADERS_SOURCE_DIR}/cmake/SPIRV-Headers.pc.in ${SPIRV_HEADERS_BINARY_DIR}/SPIRV-Headers.pc @ONLY)
    install(FILES "${SPIRV_HEADERS_BINARY_DIR}/SPIRV-Headers.pc" DESTINATION ${CMAKE_INSTALL_LIBDIR}/pkgconfig)

    set(SPIRV_HEADERS_INSTALL_DIR "${cmake_full_install_dir}")
endif ()
message(STATUS "-- -- SPIRV-Headers")
# ============ SPIRV-Headers ================================

# ============== SPIRV-Tools ================================
set(SPIRV_SKIP_TEST ON)
set(SKIP_SPIRV_TOOLS_INSTALL OFF)
add_subdirectory(SPIRV-Tools)
set(SPIRV_TOOLS_INSTALL_DIR "${cmake_full_install_dir}")
message(STATUS "-- -- SPIRV-Tools")
# ============== SPIRV-Tools ================================

# ================ glslang ==================================
set(GLSLANG_TESTS OFF)
set(ALLOW_EXTERNAL_SPIRV_TOOLS ON)
add_subdirectory(glslang)
if (SDK_INSTALL)
    set(GLSLANG_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/glslang")
    set(GLSLANG_BINARY_DIR "${CMAKE_CURRENT_BINARY_DIR}/glslang")

    ####### glslang
    install(TARGETS glslang EXPORT glslang-targets)
    set(CURRENT_GLSLANG_BINARY_DIR "${GLSLANG_BINARY_DIR}/glslang")
    if (NOT BUILD_SHARED_LIBS)
        install(TARGETS MachineIndependent EXPORT glslang-targets)
        install(TARGETS GenericCodeGen EXPORT glslang-targets)

        # Backward compatibility
        file(WRITE "${CURRENT_GLSLANG_BINARY_DIR}/glslangTargets.cmake" "
            message(WARNING \"Using `glslangTargets.cmake` is deprecated: use `find_package(glslang)` to find glslang CMake targets.\")

            if (NOT TARGET glslang::glslang)
                include(\"${CMAKE_INSTALL_FULL_LIBDIR}/cmake/glslang-targets.cmake\")
            endif()

            if(${BUILD_SHARED_LIBS})
                add_library(glslang ALIAS glslang::glslang)
            else()
                add_library(glslang ALIAS glslang::glslang)
                add_library(MachineIndependent ALIAS glslang::MachineIndependent)
                add_library(GenericCodeGen ALIAS glslang::GenericCodeGen)
            endif()
        ")
        install(FILES "${CURRENT_GLSLANG_BINARY_DIR}/glslangTargets.cmake" DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake)
    endif ()

    set(PUBLIC_HEADERS
            Public/ResourceLimits.h
            Public/ShaderLang.h
            Public/resource_limits_c.h
            Include/glslang_c_interface.h
            Include/glslang_c_shader_types.h
            Include/ResourceLimits.h
            MachineIndependent/Versions.h)

    foreach (file ${PUBLIC_HEADERS})
        get_filename_component(dir ${file} DIRECTORY)
        install(FILES "${GLSLANG_SOURCE_DIR}/glslang/${file}" DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/glslang/${dir})
    endforeach ()

    install(FILES ${GLSLANG_BUILD_INFO_H} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/glslang)

    install(TARGETS glslang-default-resource-limits EXPORT glslang-targets)

    # Backward compatibility
    file(WRITE "${CURRENT_GLSLANG_BINARY_DIR}/glslang-default-resource-limitsTargets.cmake" "
        message(WARNING \"Using `glslang-default-resource-limitsTargets.cmake` is deprecated: use `find_package(glslang)` to find glslang CMake targets.\")

        if (NOT TARGET glslang::glslang-default-resource-limits)
            include(\"\${CMAKE_INSTALL_FULL_LIBDIR}/cmake/glslang-targets.cmake\")
        endif()

        add_library(glslang-default-resource-limits ALIAS glslang::glslang-default-resource-limits)
    ")
    install(FILES "${CURRENT_GLSLANG_BINARY_DIR}/glslang-default-resource-limitsTargets.cmake" DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake)
    ####### glslang

    ####### StandAlone
    install(TARGETS glslang-standalone EXPORT glslang-targets)

    set(CURRENT_GLSLANG_BINARY_DIR "${GLSLANG_BINARY_DIR}/StandAlone")
    # Backward compatibility
    file(WRITE "${CURRENT_GLSLANG_BINARY_DIR}/glslang-standaloneTargets.cmake" "
        message(WARNING \"Using `glslang-standaloneTargets.cmake` is deprecated: use `find_package(glslang)` to find glslang CMake targets.\")

        if (NOT TARGET glslang::glslang-standalone)
            include(\"${CMAKE_INSTALL_FULL_LIBDIR}/cmake/glslang-targets.cmake\")
        endif()

        add_library(glslang-standalone ALIAS glslang::glslang-standalone)
    ")
    install(FILES "${CURRENT_GLSLANG_BINARY_DIR}/glslang-standaloneTargets.cmake" DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake)

    # Create a symbolic link to glslang named glslangValidator for backwards compatibility
    set(legacy_glslang_name "glslangValidator${CMAKE_EXECUTABLE_SUFFIX}")
    set(link_method create_symlink)
    if (WIN32 OR MINGW)
        set(link_method copy_if_different)
    endif ()

    # Create the same symlink at install time
    install(CODE "execute_process( \
                      COMMAND ${CMAKE_COMMAND} -E ${link_method} $<TARGET_FILE_NAME:glslang-standalone> ${legacy_glslang_name} \
                      WORKING_DIRECTORY \$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_BINDIR})")

    if (ENABLE_SPVREMAPPER)
        install(TARGETS spirv-remap EXPORT glslang-targets)

        # Backward compatibility
        file(WRITE "${CURRENT_GLSLANG_BINARY_DIR}/spirv-remapTargets.cmake" "
            message(WARNING \"Using `spirv-remapTargets.cmake` is deprecated: use `find_package(glslang)` to find glslang CMake targets.\")

            if (NOT TARGET glslang::spirv-remap)
                include(\"${CMAKE_INSTALL_FULL_LIBDIR}/cmake/glslang-targets.cmake\")
            endif()

            add_library(spirv-remap ALIAS glslang::spirv-remap)
        ")
        install(FILES "${CURRENT_GLSLANG_BINARY_DIR}/spirv-remapTargets.cmake" DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake)
    endif ()
    ####### StandAlone

    ####### SPIRV
    set(CURRENT_GLSLANG_BINARY_DIR "${GLSLANG_BINARY_DIR}/SPIRV")
    if (ENABLE_SPVREMAPPER)
        install(TARGETS SPVRemapper EXPORT glslang-targets)
    endif ()

    install(TARGETS SPIRV EXPORT glslang-targets)

    # Backward compatibility
    if (ENABLE_SPVREMAPPER)
        file(WRITE "${CURRENT_GLSLANG_BINARY_DIR}/SPVRemapperTargets.cmake" "
            message(WARNING \"Using `SPVRemapperTargets.cmake` is deprecated: use `find_package(glslang)` to find glslang CMake targets.\")

            if (NOT TARGET glslang::SPVRemapper)
                include(\"${CMAKE_INSTALL_FULL_LIBDIR}/cmake/glslang-targets.cmake\")
            endif()

            add_library(SPVRemapper ALIAS glslang::SPVRemapper)
        ")
        install(FILES "${CURRENT_GLSLANG_BINARY_DIR}/SPVRemapperTargets.cmake" DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake)
    endif ()

    file(WRITE "${CURRENT_GLSLANG_BINARY_DIR}/SPIRVTargets.cmake" "
        message(WARNING \"Using `SPIRVTargets.cmake` is deprecated: use `find_package(glslang)` to find glslang CMake targets.\")

        if (NOT TARGET glslang::SPIRV)
            include(\"${CMAKE_INSTALL_FULL_LIBDIR}/cmake/${PROJECT_NAME}/glslang-targets.cmake\")
        endif()

        add_library(SPIRV ALIAS glslang::SPIRV)
    ")
    install(FILES "${CURRENT_GLSLANG_BINARY_DIR}/SPIRVTargets.cmake" DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake)
    set(PUBLIC_HEADERS
            GlslangToSpv.h
            disassemble.h
            Logger.h
            spirv.hpp11
            SpvTools.h)
    foreach (file ${PUBLIC_HEADERS})
        install(FILES glslang/SPIRV/${file} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/glslang/SPIRV/)
    endforeach ()
    ####### SPIRV

    file(WRITE "${GLSLANG_BINARY_DIR}/glslang-config.cmake.in" [=[
        @PACKAGE_INIT@
        @INSTALL_CONFIG_UNIX@
        include("@PACKAGE_PATH_EXPORT_TARGETS@")
    ]=])

    set(PATH_EXPORT_TARGETS "${cmake_install_dir}/glslang-targets.cmake")
    if (UNIX OR "${CMAKE_SYSTEM_NAME}" STREQUAL "Fuchsia")
        set(INSTALL_CONFIG_UNIX [=[
            include(CMakeFindDependencyMacro)
            set(THREADS_PREFER_PTHREAD_FLAG ON)
            find_dependency(Threads REQUIRED)
        ]=])
    endif ()
    configure_package_config_file(
            "${GLSLANG_BINARY_DIR}/glslang-config.cmake.in"
            "${GLSLANG_BINARY_DIR}/glslang-config.cmake"
            PATH_VARS
            PATH_EXPORT_TARGETS
            INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake
    )

    write_basic_package_version_file("${GLSLANG_BINARY_DIR}/glslang-config-version.cmake"
            VERSION ${GLSLANG_VERSION}
            COMPATIBILITY SameMajorVersion
    )

    install(
            EXPORT glslang-targets
            NAMESPACE "glslang::"
            DESTINATION "${cmake_install_dir}"
    )

    install(
            FILES
            "${GLSLANG_BINARY_DIR}/glslang-config.cmake"
            "${GLSLANG_BINARY_DIR}/glslang-config-version.cmake"
            DESTINATION
            "${cmake_install_dir}"
    )
    set(GLSLANG_INSTALL_DIR "${cmake_full_install_dir}")
endif ()
message(STATUS "-- -- glslang")
# ================ glslang ==================================

# ======== Vulkan-ValidationLayers ==========================
add_subdirectory(Vulkan-ValidationLayers)
set(VULKAN_VALIDATIONLAYERS_INSTALL_DIR "${cmake_full_install_dir}")
message(STATUS "-- -- Vulkan-ValidationLayers")
# ======== Vulkan-ValidationLayers ==========================

# ========= Vulkan-ExtensionLayer ===========================
add_subdirectory(Vulkan-ExtensionLayer)
set(VULKAN_EXTENSIONLAYER_INSTALL_DIR "${cmake_full_install_dir}")
message(STATUS "-- -- Vulkan-ExtensionLayer")
# ========= Vulkan-ExtensionLayer ===========================

# ============== SPIRV-Cross ================================
set(SPIRV_CROSS_SHARED ON CACHE BOOL "")
set(SPIRV_CROSS_ENABLE_TESTS OFF CACHE BOOL "")
add_subdirectory(SPIRV-Cross)
set(SPIRV_CROSS_INSTALL_DIR "${cmake_full_install_dir}")
message(STATUS "-- -- SPIRV-Cross")
# ============== SPIRV-Cross ================================

# ============= SPIRV-Reflect ===============================
set(SPIRV_REFLECT_STATIC_LIB ON CACHE BOOL "")
add_subdirectory(SPIRV-Reflect)
message(STATUS "-- -- SPIRV-Reflect")
# ============= SPIRV-Reflect ===============================

# ================ shaderc ==================================
if (SDK_INSTALL)
    set(SHADERC_SKIP_INSTALL OFF)
else ()
    set(SHADERC_SKIP_INSTALL ON)
endif ()
set(SHADERC_SKIP_TESTS ON)
set(SHADERC_SKIP_EXAMPLES ON)
set(SHADERC_SKIP_COPYRIGHT_CHECK ON)
add_subdirectory(shaderc)
if (WIN32 AND NOT MSVC)
    target_link_options(shaderc_shared PRIVATE "-Wl,--allow-multiple-definition")
    target_link_options(glslc_exe PRIVATE "-Wl,--allow-multiple-definition")
endif ()
if (SDK_INSTALL)
    set(SHADERC_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/shaderc")
    set(SHADERC_BINARY_DIR "${CMAKE_CURRENT_BINARY_DIR}/shaderc")

    foreach (target IN ITEMS shaderc shaderc_util shaderc_shared shaderc_combined)
        if (TARGET ${target})
            install(TARGETS ${target} EXPORT shaderc-targets
                    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
                    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
                    BUNDLE DESTINATION ${CMAKE_INSTALL_BINDIR}
                    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR})
        else ()
            message(STATUS "Target ${target} not found")
        endif ()
    endforeach ()


    file(WRITE "${SHADERC_BINARY_DIR}/shaderc-config.cmake.in" [=[
        @PACKAGE_INIT@
        include("@PACKAGE_PATH_EXPORT_TARGETS@")
    ]=])
    set(PATH_EXPORT_TARGETS "${CMAKE_INSTALL_LIBDIR}/cmake/shaderc-targets.cmake")
    configure_package_config_file(
            "${SHADERC_BINARY_DIR}/shaderc-config.cmake.in"
            "${SHADERC_BINARY_DIR}/shaderc-config.cmake"
            PATH_VARS
            PATH_EXPORT_TARGETS
            INSTALL_DESTINATION ${cmake_install_dir}
    )

    write_basic_package_version_file("${SHADERC_BINARY_DIR}/shaderc-config-version.cmake"
            VERSION ${pack_version}
            COMPATIBILITY SameMajorVersion
    )

    install(
            EXPORT shaderc-targets
            NAMESPACE "shaderc::"
            DESTINATION "${cmake_install_dir}"
    )

    install(
            FILES
            "${SHADERC_BINARY_DIR}/shaderc-config.cmake"
            "${SHADERC_BINARY_DIR}/shaderc-config-version.cmake"
            DESTINATION
            "${cmake_install_dir}"
    )

    set(SHADERC_INSTALL_DIR "${cmake_full_install_dir}")
endif ()
message(STATUS "-- -- shaderc")
# ================ shaderc ==================================

# ================ slang ====================================
# Disable features not needed for the SDK
set(SLANG_ENABLE_TESTS OFF)
set(SLANG_ENABLE_EXAMPLES OFF)
set(SLANG_ENABLE_GFX OFF)
set(SLANG_ENABLE_SLANG_RHI OFF)
set(SLANG_ENABLE_SLANGD OFF)
set(SLANG_ENABLE_SLANGI OFF)
set(SLANG_ENABLE_REPLAYER OFF)
set(SLANG_ENABLE_PREBUILT_BINARIES OFF)
set(SLANG_ENABLE_FULL_IR_VALIDATION OFF)
set(SLANG_ENABLE_IR_BREAK_ALLOC OFF)
set(SLANG_ENABLE_ASAN OFF)
set(SLANG_ENABLE_COVERAGE OFF)
set(SLANG_ENABLE_RELEASE_LTO OFF)
set(SLANG_ENABLE_RELEASE_DEBUG_INFO OFF)
set(SLANG_ENABLE_SPLIT_DEBUG_INFO OFF)
set(SLANG_ENABLE_DX_ON_VK OFF)
set(SLANG_EXCLUDE_DAWN ON)
set(SLANG_EXCLUDE_TINT ON)
set(SLANG_SLANG_LLVM_FLAVOR "DISABLE" CACHE STRING "" FORCE)
# Use system copies already built in this composite SDK
set(SLANG_USE_SYSTEM_SPIRV_TOOLS ON)
set(SLANG_USE_SYSTEM_GLSLANG ON)
# Let slang's external/CMakeLists.txt detect existing targets
set(SLANG_USE_SYSTEM_VULKAN_HEADERS OFF)
set(SLANG_USE_SYSTEM_SPIRV_HEADERS OFF)
set(SLANG_USE_SYSTEM_UNORDERED_DENSE OFF)
set(SLANG_USE_SYSTEM_MINIZ OFF)
set(SLANG_USE_SYSTEM_LZ4 OFF)
add_subdirectory(slang)
if (SDK_INSTALL)
    set(SLANG_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/slang")
    set(SLANG_BINARY_DIR "${CMAKE_CURRENT_BINARY_DIR}/slang")

    install(DIRECTORY "${SLANG_SOURCE_DIR}/include/" DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
            PATTERN ".*" EXCLUDE)
endif ()
message(STATUS "-- -- slang")
# ================ slang ====================================
