cmake_minimum_required(VERSION 3.24)
project(OwlDependencies)

find_program(EDEPMANAGER depmanager)
if (${EDEPMANAGER} STREQUAL EDEPMANAGER-NOTFOUND)
    message(FATAL_ERROR "Dependency manager not found, go to fallback")
endif()
add_subdirectory(Libs/fmt)
add_subdirectory(Libs/spdlog)
add_subdirectory(Libs/magic_enum)
add_subdirectory(Libs/glad)

