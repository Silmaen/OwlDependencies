cmake_minimum_required(VERSION 3.24)

project(shaderc_merged VERSION ${pack_version})

add_subdirectory(SPIRV-Headers)
add_subdirectory(SPIRV-Tools)
add_subdirectory(glslang)
add_subdirectory(shaderc)
