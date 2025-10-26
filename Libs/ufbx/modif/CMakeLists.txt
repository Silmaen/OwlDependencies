cmake_minimum_required(VERSION 3.28)

set(PROJECT_ID ufbx)
set(PROJECT_VERSION 0.20.1)

project(${PROJECT_ID} VERSION ${PROJECT_VERSION} LANGUAGES C CXX)
include(GNUInstallDirs)

set(HEADER ${CMAKE_CURRENT_SOURCE_DIR}/${PROJECT_ID}.h)
add_library(${PROJECT_ID} STATIC
        ${PROJECT_ID}.c
        ${PROJECT_ID}.h
)
add_library(${PROJECT_ID}::${PROJECT_ID} ALIAS ${PROJECT_ID})

set_target_properties(${PROJECT_ID} PROPERTIES
        PUBLIC_HEADER "${HEADER}")

target_include_directories(${PROJECT_ID}
        PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>)

set(version_config ${PROJECT_BINARY_DIR}/${PROJECT_ID}-config-version.cmake)
set(project_config ${PROJECT_BINARY_DIR}/${PROJECT_ID}-config.cmake)
set(targets_export_name ${PROJECT_ID}-targets)

include(CMakePackageConfigHelpers)
write_basic_package_version_file(
        ${version_config}
        VERSION ${PROJECT_VERSION}
        COMPATIBILITY AnyNewerVersion)
configure_package_config_file(
        ${PROJECT_SOURCE_DIR}/${PROJECT_ID}-config.cmake.in
        ${project_config}
        INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_ID})

install(TARGETS ${PROJECT_ID} EXPORT ${targets_export_name}-$<CONFIG>
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
        PRIVATE_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
        FRAMEWORK DESTINATION ${CMAKE_INSTALL_BINDIR}
        CONFIGURATIONS $<CONFIG>
)

# Use a namespace because CMake provides better diagnostics for namespaced
# imported targets.
export(TARGETS ${PROJECT_ID} NAMESPACE ${PROJECT_ID}::
        FILE ${PROJECT_BINARY_DIR}/${targets_export_name}.cmake)

# Install version, config and target files.
install(
        FILES ${project_config} ${version_config}
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_ID}
)
install(EXPORT ${targets_export_name}-$<CONFIG>
        FILE ${targets_export_name}.cmake
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_ID}
        NAMESPACE ${PROJECT_ID}::)
