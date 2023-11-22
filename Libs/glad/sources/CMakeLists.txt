#
# CmakeLists for Glad
# go to https://glad.dav1d.de/ for download
#
cmake_minimum_required(VERSION 3.20)
set(PROJECT_ID glad)

if (GLAD_VERSION_1)
    set(PROJECT_VERSION "0.1.36")
else ()
    set(PROJECT_VERSION "2.0.4")
endif ()

project(glad LANGUAGES C VERSION ${PROJECT_VERSION})
include(GNUInstallDirs)

set(PROJECT_ROOT ${PROJECT_SOURCE_DIR}/${PROJECT_ID}-${PROJECT_VERSION})
if (WIN32)
    set(CMAKE_DEBUG_POSTFIX "d")
endif ()
if (GLAD_VERSION_1)
    set(SRCS ${PROJECT_ROOT}/src/glad.c)
    set(HDRS ${PROJECT_ROOT}/include/glad/glad.h ${PROJECT_ROOT}/include/KHR/khrplatform.h)
else ()
    set(SRCS ${PROJECT_ROOT}/src/gl.c ${PROJECT_ROOT}/src/vulkan.c)
    set(HDRS ${PROJECT_ROOT}/include/vk_platform.h ${PROJECT_ROOT}/include/glad/gl.h ${PROJECT_ROOT}/include/glad/vulkan.h ${PROJECT_ROOT}/include/KHR/khrplatform.h)
endif ()


add_library(${PROJECT_ID} ${SRCS})
add_library(${PROJECT_ID}::${PROJECT_ID} ALIAS ${PROJECT_ID})

target_include_directories(${PROJECT_ID} PUBLIC
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
install(TARGETS ${PROJECT_ID} EXPORT ${targets_export_name}-$<CONFIG>
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}/$<CONFIG>
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}/$<CONFIG>
        PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_ID}
        PRIVATE_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_ID}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}/$<CONFIG>
        CONFIGURATIONS $<CONFIG>
)


install(DIRECTORY ${PROJECT_ROOT}/include/glad ${PROJECT_ROOT}/include/KHR TYPE INCLUDE)
if (NOT GLAD_VERSION_1)
    install(FILES ${PROJECT_ROOT}/include/vk_platform.h TYPE INCLUDE)
endif ()

# Install version, config and target files.
install(
        FILES ${project_config} ${version_config}
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_ID}
)
install(EXPORT ${targets_export_name}-$<CONFIG>
        FILE ${targets_export_name}.cmake
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_ID}
        NAMESPACE ${PROJECT_ID}::)

