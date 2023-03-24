cmake_minimum_required(VERSION 3.20)

set(PROJECT_ID debugbreak)
set(PROJECT_VERSION 1.0)
set((PROJECT_DEST_INC debugbreak))


project(${PROJECT_ID} VERSION ${PROJECT_VERSION} LANGUAGES CXX)
include(GNUInstallDirs)

option(STB_SYSTEM_HEADERS "Expose headers with marking them as system." OFF)

set(STB_SYSTEM_HEADERS_ATTRIBUTE "")
if (STB_SYSTEM_HEADERS)
    set(STB_SYSTEM_HEADERS_ATTRIBUTE SYSTEM)
endif ()

set(HEADER ${PROJECT_ID}-${PROJECT_VERSION}/${PROJECT_ID}.h)

add_library(${PROJECT_ID} INTERFACE)
add_library(${PROJECT_ID}::${PROJECT_ID} ALIAS ${PROJECT_ID})

set_target_properties(${PROJECT_ID} PROPERTIES
        PUBLIC_HEADER "${HEADER}")

target_include_directories(${PROJECT_ID} ${STB_SYSTEM_HEADERS_ATTRIBUTE} INTERFACE
        $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/${PROJECT_ID}-${PROJECT_VERSION}>
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

install(TARGETS ${PROJECT_ID} EXPORT ${targets_export_name}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_DEST_INC}
        PRIVATE_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_DEST_INC}

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
