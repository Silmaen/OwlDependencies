
cmake_minimum_required(VERSION 3.24)

find_package(glslang REQUIRED COMPONENTS SPIRV)
add_library(glslang ALIAS glslang::glslang)
add_library(SPIRV ALIAS glslang::SPIRV)
find_package(spirv-tools REQUIRED)
add_library(SPIRV-Tools ALIAS spirv-tools::spirv-tools)


add_subdirectory(shaderc)


