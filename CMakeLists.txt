cmake_minimum_required(VERSION 3.24)
project(OwlDependencies)

find_program(EDEPMANAGER depmanager)
if (${EDEPMANAGER} STREQUAL EDEPMANAGER-NOTFOUND)
    message(FATAL_ERROR "Dependency manager not found, go to fallback")
endif()
# header-only
add_subdirectory(Libs/debugbreak)
add_subdirectory(Libs/entt)
add_subdirectory(Libs/magic_enum)
add_subdirectory(Libs/stb)
# compiled without dependency
add_subdirectory(Libs/fmt)
add_subdirectory(Libs/cpptrace)
add_subdirectory(Libs/glad)
add_subdirectory(Libs/glfw)
add_subdirectory(Libs/glm)
add_subdirectory(Libs/googletest)
add_subdirectory(Libs/jsoncpp)
add_subdirectory(Libs/nfd)
add_subdirectory(Libs/spirv-cross)
add_subdirectory(Libs/yaml-cpp)
add_subdirectory(Libs/shaderc)
add_subdirectory(Libs/tinyxml2)
# compiled with dependency
add_subdirectory(Libs/mavsdk) # depends on tinyxml2 & jsoncpp
add_subdirectory(Libs/spdlog) # depends on fmt
add_subdirectory(Libs/imgui) # depends on glfw
add_subdirectory(Libs/imguizmo) # depends on imgui

message(FATAL_ERROR)
