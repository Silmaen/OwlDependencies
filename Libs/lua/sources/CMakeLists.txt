#
# CMakeLists for Lua (official repo: github.com/lua/lua)
#
cmake_minimum_required(VERSION 3.20)
set(PROJECT_ID lua)
set(PROJECT_VERSION "5.5.0")

project(${PROJECT_ID} VERSION ${PROJECT_VERSION} LANGUAGES C)
include(GNUInstallDirs)

set(LUA_SRC_DIR ${PROJECT_SOURCE_DIR}/../${PROJECT_ID})

if (WIN32)
    set(CMAKE_DEBUG_POSTFIX "d")
endif ()

# Collect all library sources, exclude interpreter main and single-file build
file(GLOB LUA_LIB_SOURCES ${LUA_SRC_DIR}/*.c)
list(FILTER LUA_LIB_SOURCES EXCLUDE REGEX "lua\\.c$")
list(FILTER LUA_LIB_SOURCES EXCLUDE REGEX "onelua\\.c$")
list(FILTER LUA_LIB_SOURCES EXCLUDE REGEX "ltests\\.c$")

add_library(${PROJECT_ID} ${LUA_LIB_SOURCES})
add_library(${PROJECT_ID}::${PROJECT_ID} ALIAS ${PROJECT_ID})

# Platform configuration
if (UNIX)
    target_compile_definitions(${PROJECT_ID} PRIVATE LUA_USE_POSIX LUA_USE_DLOPEN)
    target_link_libraries(${PROJECT_ID} PRIVATE m dl)
endif ()
if (WIN32 AND BUILD_SHARED_LIBS)
    target_compile_definitions(${PROJECT_ID} PUBLIC LUA_BUILD_AS_DLL)
endif ()

target_include_directories(${PROJECT_ID} PUBLIC
        $<BUILD_INTERFACE:${LUA_SRC_DIR}>
        $<INSTALL_INTERFACE:include>
)

# Install targets
set(targets_export_name ${PROJECT_ID}-targets)

install(TARGETS ${PROJECT_ID} EXPORT ${targets_export_name}-$<CONFIG>
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}/$<CONFIG>
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}/$<CONFIG>
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}/$<CONFIG>
        FRAMEWORK DESTINATION ${CMAKE_INSTALL_BINDIR}/$<CONFIG>
        CONFIGURATIONS $<CONFIG>
)

# Public headers
install(FILES
        ${LUA_SRC_DIR}/lua.h
        ${LUA_SRC_DIR}/luaconf.h
        ${LUA_SRC_DIR}/lualib.h
        ${LUA_SRC_DIR}/lauxlib.h
        DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

# Package config
set(version_config ${PROJECT_BINARY_DIR}/${PROJECT_ID}-config-version.cmake)
set(project_config ${PROJECT_BINARY_DIR}/${PROJECT_ID}-config.cmake)

include(CMakePackageConfigHelpers)
write_basic_package_version_file(
        ${version_config}
        VERSION ${PROJECT_VERSION}
        COMPATIBILITY AnyNewerVersion)
configure_package_config_file(
        ${PROJECT_SOURCE_DIR}/${PROJECT_ID}-config.cmake.in
        ${project_config}
        INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_ID})

install(FILES ${project_config} ${version_config}
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_ID})
install(EXPORT ${targets_export_name}-$<CONFIG>
        FILE ${targets_export_name}.cmake
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_ID}
        NAMESPACE ${PROJECT_ID}::)
