cmake_minimum_required(VERSION 3.17.2)

project(Vulkan)

# headers part...
add_subdirectory(Vulkan-Headers)

if (NOT VK_VERSION_STRING)
    set(VK_VERSION_STRING 1.3.275)
endif ()
project(Vulkan VERSION ${VK_VERSION_STRING})

include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

install(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/Vulkan-Headers/include/vk_video" DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
install(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/Vulkan-Headers/include/vulkan" DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
# Preserve source permissions https://github.com/KhronosGroup/Vulkan-Headers/issues/336
install(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/Vulkan-Headers/registry" DESTINATION "${CMAKE_INSTALL_DATADIR}/vulkan" USE_SOURCE_PERMISSIONS)

set_target_properties(Vulkan-Headers PROPERTIES EXPORT_NAME "Headers")

install(TARGETS Vulkan-Headers EXPORT VulkanHeadersConfig INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
install(EXPORT VulkanHeadersConfig NAMESPACE "Vulkan::" DESTINATION "lib/cmake/VulkanLoader")

set(version_config "${CMAKE_CURRENT_BINARY_DIR}/Vulkan-Headers/generated/VulkanHeadersConfigVersion.cmake")
write_basic_package_version_file("${version_config}" COMPATIBILITY SameMajorVersion ARCH_INDEPENDENT)
install(FILES "${version_config}" DESTINATION "share/cmake/VulkanLoader")

set(LOADER_CODEGEN ON)
add_subdirectory(Vulkan-Loader)


