cmake_minimum_required(VERSION 3.20 FATAL_ERROR)

set(PROJECT_VERSION "0.1")
set(PROJECT_ID imgui)


project(${PROJECT_ID} VERSION ${PROJECT_VERSION} LANGUAGES CXX)
include(GNUInstallDirs)

set(PROJECT_ROOT ${PROJECT_SOURCE_DIR}/${PROJECT_ID}-docking)

file(GLOB SRCS
        ${PROJECT_ROOT}/*.cpp
        )
file(GLOB HDRS
        ${PROJECT_ROOT}/*.h
        )

add_library(${PROJECT_ID} ${SRCS} ${HDRS})
add_library(${PROJECT_ID}::${PROJECT_ID} ALIAS ${PROJECT_ID})

target_include_directories(${PROJECT_ID} PRIVATE ${PROJECT_ROOT} ${PROJECT_ROOT}/backend)

target_compile_definitions(${PROJECT_ID} INTERFACE IMGUI_IMPL_HAS_DOCKING)

target_include_directories(${PROJECT_ID} SYSTEM INTERFACE
        $<BUILD_INTERFACE:${PROJECT_ROOT}>
        $<INSTALL_INTERFACE:include>
        )

# glfw dependency
find_package(glfw3 REQUIRED)
target_link_libraries(${PROJECT_ID} PRIVATE glfw3::glfw3)
target_sources(imgui PRIVATE ${PROJECT_ROOT}/backends/imgui_impl_glfw.cpp ${PROJECT_ROOT}/backends/imgui_impl_glfw.h)

# opengl dependency
target_compile_definitions(${PROJECT_ID} PUBLIC IMGUI_IMPL_OPENGL_LOADER_GLAD)
target_sources(imgui PRIVATE ${PROJECT_ROOT}/backends/imgui_impl_opengl3.cpp ${PROJECT_ROOT}/backends/imgui_impl_opengl3.h ${PROJECT_ROOT}/backends/imgui_impl_opengl3_loader.h)

# windows
if (${CMAKE_SYSTEM_NAME} MATCHES "Windows")
    target_link_libraries(${PROJECT_ID} PRIVATE dwmapi)
    target_sources(imgui PRIVATE ${PROJECT_ROOT}/backends/imgui_impl_win32.cpp ${PROJECT_ROOT}/backends/imgui_impl_win32.h)
endif ()

file(GLOB PUBLIC_HEADERS
        ${PROJECT_ROOT}/*.h
        ${PROJECT_ROOT}/backends/*.h
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

