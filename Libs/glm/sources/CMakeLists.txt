cmake_minimum_required(VERSION 3.20 FATAL_ERROR)

set(PROJECT_VERSION "0.9.9.8")
set(PROJECT_ID glm)


project(${PROJECT_ID} VERSION ${PROJECT_VERSION} LANGUAGES CXX)
include(GNUInstallDirs)

set(PROJECT_ROOT ${PROJECT_SOURCE_DIR}/${PROJECT_ID})

add_subdirectory(${PROJECT_ROOT}/glm)
add_library(${PROJECT_ID}::${PROJECT_ID} ALIAS ${PROJECT_ID})

target_include_directories(${PROJECT_ID} SYSTEM INTERFACE
        $<BUILD_INTERFACE:${PROJECT_ROOT}/glm>
        $<INSTALL_INTERFACE:include>
        )

file(GLOB_RECURSE PUBLIC_HEADERS
        ${PROJECT_ROOT}/glm/*.h
        ${PROJECT_ROOT}/glm/*.hpp
        ${PROJECT_ROOT}/glm/*.inl
        )

set_target_properties(${PROJECT_ID} PROPERTIES
        PUBLIC_HEADER "${PUBLIC_HEADERS}"
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
if (BUILD_STATIC_LIBS)
    install(TARGETS ${PROJECT_ID}_static EXPORT ${targets_export_name}
            LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
            ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
            PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_ID}
            PRIVATE_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_ID}
            RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
endif ()
if (BUILD_SHARED_LIBS)
    install(TARGETS ${PROJECT_ID}_shared EXPORT ${targets_export_name}
            LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
            ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
            PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_ID}
            PRIVATE_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_ID}
            RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
endif ()
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


