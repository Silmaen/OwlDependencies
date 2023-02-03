cmake_minimum_required(VERSION 3.24)
project(OwlDependencies)

find_package("Python" REQUIRED)

add_custom_target(regenerate ALL
        COMMAND ${Python_EXECUTABLE} -u ${CMAKE_SOURCE_DIR}/PyUtility/regenerate.py
        USES_TERMINAL)
