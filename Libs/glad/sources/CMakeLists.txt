#
# CmakeLists for Glad
# go to https://glad.dav1d.de/ for download
#
cmake_minimum_required(VERSION 3.20)
set(PROJECT_VERSION "0.1.36")
set(PROJECT_ID glad)


project(glad LANGUAGES C VERSION ${PROJECT_VERSION})
include(GNUInstallDirs)

set(PROJECT_ROOT ${PROJECT_SOURCE_DIR}/${PROJECT_ID}-${PROJECT_VERSION})

set(SRCS ${PROJECT_ROOT}/src/glad.c ${PROJECT_ROOT}/include/glad/glad.h ${PROJECT_ROOT}/include/KHR/khrplatform.h)

add_library(${PROJECT_ID} ${SRCS})
add_library(${PROJECT_ID}::${PROJECT_ID} ALIAS ${PROJECT_ID})

target_include_directories(${PROJECT_ID} PRIVATE ${PROJECT_ROOT}/include)

target_include_directories(${PROJECT_ID} SYSTEM INTERFACE
        $<BUILD_INTERFACE:${PROJECT_ROOT}/include>
        $<INSTALL_INTERFACE:include>
        )

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

install(TARGETS ${PROJECT_ID} EXPORT ${targets_export_name}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_ID}
        PRIVATE_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_ID}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
# Use a namespace because CMake provides better diagnostics for namespaced
# imported targets.
export(TARGETS ${PROJECT_ID} NAMESPACE ${PROJECT_ID}::
        FILE ${PROJECT_BINARY_DIR}/${targets_export_name}.cmake)

# Install version, config and target files.
install(
        FILES ${project_config} ${version_config}
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_ID}
)
install(EXPORT ${targets_export_name} DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_ID}
        NAMESPACE ${PROJECT_ID}::)

