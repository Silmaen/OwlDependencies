
set(SUPERBUILD OFF CACHE BOOL "bbb")
set(BUILD_TESTS OFF CACHE BOOL "bbb")

# Only some third party management
include(MAVSDK/third_party/cmake/build_target.cmake)
set(DEPS_BUILD_PATH "${PROJECT_BINARY_DIR}/third_party" CACHE PATH "Install path for the dependencies. Ignored if SUPERBUILD=OFF.")
set(DEPS_INSTALL_PATH "${DEPS_BUILD_PATH}/install" CACHE PATH "Install path for the dependencies. Ignored if SUPERBUILD=OFF.")
set(PROJECT_SOURCE_DIR_BACK ${PROJECT_SOURCE_DIR})
set(PROJECT_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/MAVSDK/third_party)
build_target(mavlink)
set(PROJECT_SOURCE_DIR ${PROJECT_SOURCE_DIR_BACK})
# end 3rd Party

add_subdirectory(MAVSDK)
