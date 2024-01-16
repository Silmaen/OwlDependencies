cmake_minimum_required(VERSION 3.20 FATAL_ERROR)

set(PROJECT_VERSION "1.84")
set(PROJECT_ID imguizmo)


project(${PROJECT_ID} VERSION ${PROJECT_VERSION} LANGUAGES CXX)
include(GNUInstallDirs)

set(PROJECT_ROOT ${PROJECT_SOURCE_DIR}/${PROJECT_ID})

file(GLOB SRCS
        ${PROJECT_ROOT}/*.cpp
)
file(GLOB HDRS
        ${PROJECT_ROOT}/*.h
)


add_library(${PROJECT_ID} ${SRCS} ${HDRS})
add_library(${PROJECT_ID}::${PROJECT_ID} ALIAS ${PROJECT_ID})


target_include_directories(${PROJECT_ID} SYSTEM INTERFACE
        $<BUILD_INTERFACE:${PROJECT_ROOT}>
        $<INSTALL_INTERFACE:include>
)

# imgui dependency
find_package(VulkanHeaders REQUIRED)
find_package(VulkanLoader REQUIRED)
find_package(imgui REQUIRED)
target_link_libraries(${PROJECT_ID} PRIVATE imgui::imgui)
target_include_directories(${PROJECT_ID} PRIVATE ${imgui_INCLUDE_DIRS}/imgui)

file(GLOB PUBLIC_HEADERS
        ${PROJECT_ROOT}/*.h
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

install(TARGETS ${PROJECT_ID} EXPORT ${targets_export_name}-$<CONFIG>
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}/$<CONFIG>
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}/$<CONFIG>
        PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
        PRIVATE_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}/$<CONFIG>
        FRAMEWORK DESTINATION ${CMAKE_INSTALL_BINDIR}/$<CONFIG>
        CONFIGURATIONS $<CONFIG>
)

# Install version, config and target files.
install(
        FILES ${project_config} ${version_config}
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_ID}
)
install(EXPORT ${targets_export_name}-$<CONFIG>
        FILE ${targets_export_name}.cmake
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_ID}
        NAMESPACE ${PROJECT_ID}::)


