#
# CmakeLists for Glad
# go to https://glad.dav1d.de/ for download
#
cmake_minimum_required(VERSION 3.20)
set(GLAD_VERSION 0.1.36)


project(glad LANGUAGES C VERSION ${GLAD_VERSION})
include(GNUInstallDirs)


set(GLAD_SOURCE glad-${GLAD_VERSION}/src/glad.c glad-${GLAD_VERSION}/include/glad/glad.h glad-${GLAD_VERSION}/include/KHR/khrplatform.h)
add_library(glad ${GLAD_SOURCE})
add_library(glad::glad ALIAS glad)

target_include_directories(glad PRIVATE ${PROJECT_SOURCE_DIR}/glad-${GLAD_VERSION}/include)
target_include_directories(glad SYSTEM INTERFACE
        $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/glad-${GLAD_VERSION}/include>
        $<INSTALL_INTERFACE:include>
        )

set(version_config ${PROJECT_BINARY_DIR}/glad-config-version.cmake)
set(project_config ${PROJECT_BINARY_DIR}/glad-config.cmake)
set(targets_export_name glad-targets)

include(CMakePackageConfigHelpers)
write_basic_package_version_file(
        ${version_config}
        VERSION ${GLAD_VERSION}
        COMPATIBILITY AnyNewerVersion)
configure_package_config_file(
        ${PROJECT_SOURCE_DIR}/glad-config.cmake.in
        ${project_config}
        INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/glad)

install(TARGETS glad EXPORT ${targets_export_name}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/glad
        PRIVATE_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/glad

        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})

# Use a namespace because CMake provides better diagnostics for namespaced
# imported targets.
export(TARGETS glad NAMESPACE glad::
        FILE ${PROJECT_BINARY_DIR}/${targets_export_name}.cmake)

# Install version, config and target files.
install(
        FILES ${project_config} ${version_config}
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/glad
)
install(EXPORT ${targets_export_name} DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/glad
        NAMESPACE glad::)

