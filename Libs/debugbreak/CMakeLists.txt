cmake_minimum_required(VERSION 3.20)

project(debugbreak CXX)
include(GNUInstallDirs)

option(DBR_SYSTEM_HEADERS "Expose headers with marking them as system." OFF)

set(DBR_SYSTEM_HEADERS_ATTRIBUTE "")
if (DBR_SYSTEM_HEADERS)
    set(DBR_SYSTEM_HEADERS_ATTRIBUTE SYSTEM)
endif ()

set(HEADER debugbreak-1.0/debugbreak.h)

add_library(debugbreak INTERFACE)
add_library(debugbreak::debugbreak ALIAS debugbreak)

set_target_properties(debugbreak PROPERTIES
        PUBLIC_HEADER "${HEADER}")

target_include_directories(debugbreak ${DBR_SYSTEM_HEADERS_ATTRIBUTE} INTERFACE
        $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/debugbreak-1.0>
        $<INSTALL_INTERFACE:include>)

set(version_config ${PROJECT_BINARY_DIR}/debugbreak-config-version.cmake)
set(project_config ${PROJECT_BINARY_DIR}/debugbreak-config.cmake)
set(targets_export_name debugbreak-targets)

include(CMakePackageConfigHelpers)
write_basic_package_version_file(
        ${version_config}
        VERSION 1.0
        COMPATIBILITY AnyNewerVersion)
configure_package_config_file(
        ${PROJECT_SOURCE_DIR}/debugbreak-config.cmake.in
        ${project_config}
        INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/debugbreak)

install(TARGETS debugbreak EXPORT ${targets_export_name}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/debugbreak
        PRIVATE_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/debugbreak

        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})

# Use a namespace because CMake provides better diagnostics for namespaced
# imported targets.
export(TARGETS debugbreak NAMESPACE debugbreak::
        FILE ${PROJECT_BINARY_DIR}/${targets_export_name}.cmake)

# Install version, config and target files.
install(
        FILES ${project_config} ${version_config}
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/debugbreak
)
install(EXPORT ${targets_export_name} DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/debugbreak
        NAMESPACE debugbreak::)
