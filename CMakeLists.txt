cmake_minimum_required(VERSION 3.24)
project(OwlDependencies)

find_program(EDEPMANAGER depmanager)
if (${EDEPMANAGER} STREQUAL EDEPMANAGER-NOTFOUND)
    message(FATAL_ERROR "Dependency manager not found, go to fallback")
endif ()
# header-only
add_subdirectory(Libs/debugbreak)
add_subdirectory(Libs/entt)
add_subdirectory(Libs/magic_enum)
add_subdirectory(Libs/stb)
add_subdirectory(Libs/zeus)
# compiled without dependency
add_subdirectory(Libs/box2d)
add_subdirectory(Libs/brotli)
add_subdirectory(Libs/fmt)
add_subdirectory(Libs/curl)
add_subdirectory(Libs/glad)
add_subdirectory(Libs/glfw)
add_subdirectory(Libs/glm)
add_subdirectory(Libs/googletest)
add_subdirectory(Libs/harfbuzz)
add_subdirectory(Libs/jsoncpp)
add_subdirectory(Libs/nfd)
add_subdirectory(Libs/openal)
add_subdirectory(Libs/yaml-cpp)
add_subdirectory(Libs/tinygltf)
add_subdirectory(Libs/tinyobjloader)
add_subdirectory(Libs/tinyply)
add_subdirectory(Libs/tinyxml2)
add_subdirectory(Libs/vulkan_sdk)
add_subdirectory(Libs/zlib)
add_subdirectory(Libs/zstd)
# compiled with dependency
add_subdirectory(Libs/libpng) # depends on zlib
add_subdirectory(Libs/libdwarf) # depends on zstd
add_subdirectory(Libs/cpptrace) # depends on libdwarf
add_subdirectory(Libs/mavsdk) # depends on tinyxml2 & jsoncpp
add_subdirectory(Libs/spdlog) # depends on fmt
add_subdirectory(Libs/imgui) # depends on glfw & vulkan
add_subdirectory(Libs/imguizmo) # depends on imgui
add_subdirectory(Libs/FreeType) # depends on libpng, harfbuzz & brotli
add_subdirectory(Libs/msdfgen)
add_subdirectory(Libs/msdf-atlas-gen)
